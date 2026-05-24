import random
from datetime import datetime

from sqlalchemy import delete, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.exception import ServiceException
from module_drama.entity.do.drama_do import (
    Drama,
    DramaAd,
    DramaComment,
    DramaUserChoiceLog,
    DramaUserFavorite,
    DramaUserLike,
    DramaUserSubscribe,
    DramaUserWatchHistory,
    DramaVideoChoice,
    DramaVideoNode,
    DramaVideoReview,
)
from module_drama.entity.vo.drama_vo import (
    ChoiceLogIn,
    CommentCreateModel,
    FavoriteIn,
    LikeIn,
    ReviewCreateModel,
    WatchHistoryIn,
)


def _effective_ad_media(ad: DramaAd) -> str | None:
    return ad.media_url or ad.image_url


class DramaAppContentService:
    """C 端内容/互动"""

    @staticmethod
    def _node_visible_app():
        return (DramaVideoNode.status == 'published') & (DramaVideoNode.review_status == 'approved')

    @classmethod
    async def feed(cls, db: AsyncSession, page_num: int, page_size: int) -> list[dict]:
        """信息流：已通过审的节点视频 + 广告穿插"""
        stmt = (
            select(DramaVideoNode, Drama)
            .join(Drama, Drama.drama_id == DramaVideoNode.drama_id)
            .where(Drama.status == 'published', cls._node_visible_app())
            .order_by(DramaVideoNode.create_time.desc())
            .offset((page_num - 1) * page_size)
            .limit(page_size)
        )
        rows = (await db.execute(stmt)).all()
        ads = (
            (await db.execute(select(DramaAd).where(DramaAd.status == '0').order_by(DramaAd.weight.desc()).limit(50)))
            .scalars()
            .all()
        )
        ads_active = [a for a in ads if cls._ad_time_ok(a)]
        random.shuffle(ads_active)  # true random rotation per feed call
        items: list[dict] = []
        ad_idx = 0
        for i, (n, d) in enumerate(rows):
            items.append(
                {
                    'kind': 'video',
                    'drama': {
                        'drama_id': d.drama_id,
                        'title': d.title,
                        'cover_url': d.cover_url,
                        'description': d.description,
                        'drama_type': d.drama_type,
                        'tags': d.tags,
                        'heat': d.heat,
                    },
                    'node': {
                        'node_id': n.node_id,
                        'title': n.title,
                        'video_url': n.video_url,
                        'cover_url': n.cover_url,
                        'duration_sec': n.duration_sec,
                        'episode_no': n.episode_no,
                        'is_interactive': n.is_interactive,
                        'choice_trigger_sec': n.choice_trigger_sec,
                    },
                }
            )
            if ads_active and (i + 1) % 3 == 0:
                a = ads_active[ad_idx % len(ads_active)]
                ad_idx += 1
                items.append(
                    {
                        'kind': 'ad',
                        'ad': cls._ad_public_dict(a),
                    }
                )
        return items

    @classmethod
    def _ad_time_ok(cls, a: DramaAd) -> bool:
        now = datetime.now()
        if a.start_time and now < a.start_time:
            return False
        return not (a.end_time and now > a.end_time)

    @classmethod
    def _ad_public_dict(cls, a: DramaAd) -> dict:
        return {
            'ad_id': a.ad_id,
            'title': a.title,
            'media_type': a.media_type,
            'media_url': _effective_ad_media(a),
            'cover_url': a.cover_url,
            'image_url': a.image_url,
            'link_url': a.link_url,
            'slot_type': a.slot_type,
        }

    @classmethod
    async def list_dramas(
        cls,
        db: AsyncSession,
        drama_type: str | None = None,
        keyword: str | None = None,
        sort: str | None = None,
        page_num: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Drama], int]:
        """返回 (dramas, total_count)"""
        q = select(Drama).where(Drama.status == 'published')
        count_q = select(func.count()).select_from(Drama).where(Drama.status == 'published')
        # Apply sort order
        if sort == 'heat':
            q = q.order_by(Drama.heat.desc(), Drama.drama_id.desc())
        elif sort == 'latest':
            q = q.order_by(Drama.create_time.desc(), Drama.drama_id.desc())
        else:
            # recommend (default): admin-defined sort rank
            q = q.order_by(Drama.sort.desc(), Drama.drama_id.desc())
        if drama_type:
            q = q.where(Drama.drama_type == drama_type)
            count_q = count_q.where(Drama.drama_type == drama_type)
        if keyword:
            kw = f'%{keyword.strip()}%'
            q = q.where(or_(Drama.title.like(kw), Drama.description.like(kw), Drama.tags.like(kw)))
            count_q = count_q.where(or_(Drama.title.like(kw), Drama.description.like(kw), Drama.tags.like(kw)))
        # total count
        total = int((await db.execute(count_q)).scalar() or 0)
        # paginated results
        q = q.offset((page_num - 1) * page_size).limit(page_size)
        r = await db.execute(q)
        return list(r.scalars().all()), total

    @classmethod
    async def list_episodes(cls, db: AsyncSession, drama_id: int) -> list[DramaVideoNode]:
        r = await db.execute(
            select(DramaVideoNode)
            .where(
                DramaVideoNode.drama_id == drama_id,
                DramaVideoNode.status == 'published',
                DramaVideoNode.review_status == 'approved',
            )
            .order_by(
                DramaVideoNode.episode_no.is_(None),
                DramaVideoNode.episode_no,
                DramaVideoNode.sort,
                DramaVideoNode.node_id,
            )
        )
        return list(r.scalars().all())

    @classmethod
    async def get_drama(cls, db: AsyncSession, drama_id: int) -> Drama:
        r = await db.execute(select(Drama).where(Drama.drama_id == drama_id))
        d = r.scalars().first()
        if not d or d.status != 'published':
            raise ServiceException(data='', message='短剧不存在或未发布')
        return d

    @classmethod
    async def entry_node(cls, db: AsyncSession, drama_id: int) -> DramaVideoNode | None:
        vis = cls._node_visible_app()
        # Single query: prioritize is_entry='1', then fallback to episode_no/sort ordering
        r = await db.execute(
            select(DramaVideoNode)
            .where(DramaVideoNode.drama_id == drama_id, vis)
            .order_by(
                (DramaVideoNode.is_entry == '1').desc(),  # entry node first
                DramaVideoNode.episode_no.is_(None),
                DramaVideoNode.episode_no,
                DramaVideoNode.sort,
                DramaVideoNode.node_id,
            )
            .limit(1)
        )
        return r.scalars().first()

    @classmethod
    async def get_node(cls, db: AsyncSession, node_id: int) -> DramaVideoNode:
        r = await db.execute(select(DramaVideoNode).where(DramaVideoNode.node_id == node_id))
        n = r.scalars().first()
        if not n or n.status != 'published' or n.review_status != 'approved':
            raise ServiceException(data='', message='节点不存在或未上架')
        return n

    @classmethod
    async def list_choices(cls, db: AsyncSession, node_id: int) -> list[DramaVideoChoice]:
        r = await db.execute(
            select(DramaVideoChoice)
            .where(DramaVideoChoice.node_id == node_id)
            .order_by(DramaVideoChoice.sort, DramaVideoChoice.choice_id)
        )
        return list(r.scalars().all())

    @classmethod
    async def list_ads(cls, db: AsyncSession, slot: str | None) -> list[DramaAd]:
        now = datetime.now()
        q = select(DramaAd).where(DramaAd.status == '0')
        if slot:
            q = q.where(DramaAd.slot_type == slot)
        q = q.where(or_(DramaAd.start_time.is_(None), DramaAd.start_time <= now))
        q = q.where(or_(DramaAd.end_time.is_(None), DramaAd.end_time >= now))
        r = await db.execute(q.order_by(DramaAd.weight.desc()))
        return list(r.scalars().all())

    @classmethod
    async def ad_impression(cls, db: AsyncSession, ad_id: int) -> None:
        await db.execute(
            update(DramaAd).where(DramaAd.ad_id == ad_id).values(impression_count=DramaAd.impression_count + 1)
        )
        await db.commit()

    @classmethod
    async def ad_click(cls, db: AsyncSession, ad_id: int) -> None:
        await db.execute(update(DramaAd).where(DramaAd.ad_id == ad_id).values(click_count=DramaAd.click_count + 1))
        await db.commit()

    @classmethod
    async def upsert_watch(cls, db: AsyncSession, user_id: int, body: WatchHistoryIn) -> None:
        r = await db.execute(
            select(DramaUserWatchHistory).where(
                DramaUserWatchHistory.app_user_id == user_id,
                DramaUserWatchHistory.drama_id == body.drama_id,
            )
        )
        row = r.scalars().first()
        if row:
            row.node_id = body.node_id
            row.progress_sec = body.progress_sec
        else:
            db.add(
                DramaUserWatchHistory(
                    app_user_id=user_id,
                    drama_id=body.drama_id,
                    node_id=body.node_id,
                    progress_sec=body.progress_sec,
                )
            )
        await db.commit()

    @classmethod
    async def list_history(cls, db: AsyncSession, user_id: int) -> list[dict]:
        r = await db.execute(
            select(DramaUserWatchHistory, Drama)
            .join(Drama, Drama.drama_id == DramaUserWatchHistory.drama_id)
            .where(DramaUserWatchHistory.app_user_id == user_id)
            .order_by(DramaUserWatchHistory.update_time.desc())
        )
        out = []
        for h, d in r.all():
            out.append(
                {
                    'drama_id': d.drama_id,
                    'title': d.title,
                    'cover_url': d.cover_url,
                    'node_id': h.node_id,
                    'progress_sec': h.progress_sec,
                }
            )
        return out

    @classmethod
    async def toggle_like(cls, db: AsyncSession, user_id: int, body: LikeIn) -> dict:
        r = await db.execute(
            select(DramaUserLike).where(
                DramaUserLike.app_user_id == user_id,
                DramaUserLike.target_type == body.target_type,
                DramaUserLike.target_id == body.target_id,
            )
        )
        exists = r.scalars().first()
        if exists:
            await db.execute(
                delete(DramaUserLike).where(
                    DramaUserLike.app_user_id == user_id,
                    DramaUserLike.target_type == body.target_type,
                    DramaUserLike.target_id == body.target_id,
                )
            )
            await db.commit()
            return {'liked': False}
        db.add(
            DramaUserLike(
                app_user_id=user_id,
                target_type=body.target_type,
                target_id=body.target_id,
            )
        )
        await db.commit()
        return {'liked': True}

    @classmethod
    async def toggle_favorite(cls, db: AsyncSession, user_id: int, body: FavoriteIn) -> dict:
        r = await db.execute(
            select(DramaUserFavorite).where(
                DramaUserFavorite.app_user_id == user_id,
                DramaUserFavorite.drama_id == body.drama_id,
            )
        )
        exists = r.scalars().first()
        if exists:
            await db.execute(
                delete(DramaUserFavorite).where(
                    DramaUserFavorite.app_user_id == user_id,
                    DramaUserFavorite.drama_id == body.drama_id,
                )
            )
            await db.commit()
            return {'favorited': False}
        db.add(DramaUserFavorite(app_user_id=user_id, drama_id=body.drama_id))
        await db.commit()
        return {'favorited': True}

    @classmethod
    async def is_drama_favorited(cls, db: AsyncSession, user_id: int, drama_id: int) -> bool:
        r = await db.execute(
            select(DramaUserFavorite).where(
                DramaUserFavorite.app_user_id == user_id,
                DramaUserFavorite.drama_id == drama_id,
            )
        )
        return r.scalars().first() is not None

    @classmethod
    async def list_favorites(cls, db: AsyncSession, user_id: int) -> list[dict]:
        r = await db.execute(
            select(DramaUserFavorite, Drama)
            .join(Drama, Drama.drama_id == DramaUserFavorite.drama_id)
            .where(DramaUserFavorite.app_user_id == user_id)
            .order_by(DramaUserFavorite.create_time.desc())
        )
        out = []
        for f, d in r.all():
            out.append(
                {
                    'drama_id': d.drama_id,
                    'title': d.title,
                    'cover_url': d.cover_url,
                    'drama_type': d.drama_type,
                    'tags': d.tags,
                    'heat': d.heat,
                    'create_time': f.create_time,
                }
            )
        return out

    @classmethod
    async def user_has_liked(cls, db: AsyncSession, user_id: int, target_type: str, target_id: int) -> bool:
        r = await db.execute(
            select(DramaUserLike).where(
                DramaUserLike.app_user_id == user_id,
                DramaUserLike.target_type == target_type,
                DramaUserLike.target_id == target_id,
            )
        )
        return r.scalars().first() is not None

    @classmethod
    async def add_comment(cls, db: AsyncSession, user_id: int, body: CommentCreateModel) -> None:
        db.add(
            DramaComment(
                app_user_id=user_id,
                drama_id=body.drama_id,
                node_id=body.node_id,
                content=body.content,
            )
        )
        await db.commit()

    @classmethod
    async def list_comments(cls, db: AsyncSession, drama_id: int) -> list[dict]:
        r = await db.execute(
            select(DramaComment)
            .where(DramaComment.drama_id == drama_id, DramaComment.status == '0')
            .order_by(DramaComment.create_time.desc())
            .limit(100)
        )
        comments = list(r.scalars().all())
        if not comments:
            return []
        # Batch-fetch like counts in a single query to avoid N+1
        comment_ids = [c.comment_id for c in comments]
        like_counts_r = await db.execute(
            select(DramaUserLike.target_id, func.count())
            .where(DramaUserLike.target_type == 'comment', DramaUserLike.target_id.in_(comment_ids))
            .group_by(DramaUserLike.target_id)
        )
        like_counts_map = dict(like_counts_r.all())
        out = []
        for c in comments:
            out.append(
                {
                    'comment_id': c.comment_id,
                    'app_user_id': c.app_user_id,
                    'drama_id': c.drama_id,
                    'node_id': c.node_id,
                    'content': c.content,
                    'like_count': like_counts_map.get(c.comment_id, 0),
                    'status': c.status,
                    'create_time': c.create_time.isoformat() if c.create_time else None,
                }
            )
        return out

    @classmethod
    async def log_choice(cls, db: AsyncSession, user_id: int, body: ChoiceLogIn) -> None:
        db.add(
            DramaUserChoiceLog(
                app_user_id=user_id,
                drama_id=body.drama_id,
                from_node_id=body.from_node_id,
                choice_id=body.choice_id,
                to_node_id=body.to_node_id,
            )
        )
        await db.commit()

    @classmethod
    async def submit_review(cls, db: AsyncSession, user_id: int, body: ReviewCreateModel) -> None:
        db.add(
            DramaVideoReview(
                app_user_id=user_id,
                drama_id=body.drama_id,
                node_id=body.node_id,
                rating=body.rating,
                content=body.content,
                status='pending',
            )
        )
        await db.commit()

    @classmethod
    async def like_count(cls, db: AsyncSession, target_type: str, target_id: int) -> int:
        r = await db.execute(
            select(func.count())
            .select_from(DramaUserLike)
            .where(DramaUserLike.target_type == target_type, DramaUserLike.target_id == target_id)
        )
        return int(r.scalar() or 0)

    @classmethod
    async def user_dashboard_counts(cls, db: AsyncSession, user_id: int) -> dict:
        """我的页统计：观看记录条数、收藏数、点赞次数、追剧（观看中出现过的剧目数）"""
        r_wh = await db.execute(
            select(func.count()).select_from(DramaUserWatchHistory).where(DramaUserWatchHistory.app_user_id == user_id)
        )
        r_fav = await db.execute(
            select(func.count()).select_from(DramaUserFavorite).where(DramaUserFavorite.app_user_id == user_id)
        )
        r_like = await db.execute(
            select(func.count()).select_from(DramaUserLike).where(DramaUserLike.app_user_id == user_id)
        )
        r_chase = await db.execute(
            select(func.count(func.distinct(DramaUserSubscribe.drama_id))).where(
                DramaUserSubscribe.app_user_id == user_id
            )
        )
        return {
            'watch_history_count': int(r_wh.scalar() or 0),
            'favorite_count': int(r_fav.scalar() or 0),
            'like_count': int(r_like.scalar() or 0),
            'watching_drama_count': int(r_chase.scalar() or 0),
        }

    @classmethod
    async def toggle_subscribe(cls, db: AsyncSession, user_id: int, drama_id: int, notify_enabled: bool = True) -> dict:
        """追更订阅/取消订阅，返回 {subscribed: bool}"""
        existing = await db.execute(
            select(DramaUserSubscribe).where(
                DramaUserSubscribe.app_user_id == user_id,
                DramaUserSubscribe.drama_id == drama_id,
            )
        )
        sub = existing.scalars().first()
        if sub:
            await db.delete(sub)
            await db.commit()
            return {'subscribed': False}
        new_sub = DramaUserSubscribe(
            app_user_id=user_id, drama_id=drama_id, notify_enabled='1' if notify_enabled else '0'
        )
        db.add(new_sub)
        await db.commit()
        return {'subscribed': True}

    @classmethod
    async def list_subscriptions(cls, db: AsyncSession, user_id: int) -> list[dict]:
        """我的追更列表，返回剧目信息"""
        rows = await db.execute(
            select(DramaUserSubscribe, Drama)
            .join(Drama, Drama.drama_id == DramaUserSubscribe.drama_id)
            .where(DramaUserSubscribe.app_user_id == user_id, Drama.status == 'published')
            .order_by(DramaUserSubscribe.create_time.desc())
        )
        return [
            {
                'subscribe_id': sub.subscribe_id,
                'drama_id': d.drama_id,
                'title': d.title,
                'cover_url': d.cover_url,
                'drama_type': d.drama_type,
                'notify_enabled': sub.notify_enabled == '1',
                'create_time': sub.create_time.isoformat() if sub.create_time else None,
            }
            for sub, d in rows.all()
        ]

    @classmethod
    async def check_new_episodes(cls, db: AsyncSession, user_id: int, drama_id: int) -> dict:
        """检查某剧的追更是否有新集更新"""
        sub_row = await db.execute(
            select(DramaUserSubscribe).where(
                DramaUserSubscribe.app_user_id == user_id,
                DramaUserSubscribe.drama_id == drama_id,
            )
        )
        sub = sub_row.scalars().first()
        if not sub:
            return {'subscribed': False, 'has_new': False}
        last_node_row = await db.execute(
            select(DramaVideoNode)
            .where(DramaVideoNode.drama_id == drama_id, cls._node_visible_app())
            .order_by(DramaVideoNode.create_time.desc())
            .limit(1)
        )
        last_node = last_node_row.scalars().first()
        has_new = False
        if last_node and sub.create_time and last_node.create_time and last_node.create_time > sub.create_time:
            has_new = True
        return {'subscribed': True, 'has_new': has_new, 'last_episode_title': last_node.title if last_node else None}
