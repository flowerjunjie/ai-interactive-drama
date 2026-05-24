from datetime import datetime

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from common.constant import CommonConstant
from exceptions.exception import ServiceException
from module_drama.entity.do.drama_do import (
    Drama,
    DramaAd,
    DramaAppUser,
    DramaComment,
    DramaUploadFile,
    DramaUserFavorite,
    DramaUserWatchHistory,
    DramaVideoChoice,
    DramaVideoNode,
    DramaVideoReview,
)
from module_drama.entity.vo.drama_vo import (
    DramaAdSaveModel,
    DramaSaveModel,
    NodeModerationRejectModel,
    ReviewAuditModel,
    UploadCompleteIn,
    VideoChoiceSaveModel,
    VideoNodeSaveModel,
)
from module_drama.service.app_auth_service import DramaAppAuthService
from module_drama.service.tos_service import DramaTosService
from utils.page_util import PageUtil


class DramaAdminService:
    _PAD = CommonConstant.DRAMA_AD_STATUS_ACTIVE
    _NA = CommonConstant.DRAMA_NODE_REVIEW_APPROVED
    _NR = CommonConstant.DRAMA_NODE_REVIEW_REJECTED
    _RVP = CommonConstant.DRAMA_REVIEW_STATUS_PENDING
    _UPP = CommonConstant.DRAMA_UPLOAD_STATUS_PENDING

    @classmethod
    async def dashboard(cls, db: AsyncSession) -> dict:
        c_drama = await db.execute(select(func.count()).select_from(Drama))
        c_node = await db.execute(select(func.count()).select_from(DramaVideoNode))
        c_review = await db.execute(
            select(func.count()).select_from(DramaVideoReview).where(DramaVideoReview.status == cls._RVP)
        )
        c_pending_nodes = await db.execute(
            select(func.count()).select_from(DramaVideoNode).where(DramaVideoNode.review_status == cls._RVP)
        )
        c_users = await DramaAppAuthService.count_users(db)
        today = func.curdate()
        c_watch_today = await db.execute(
            select(func.count())
            .select_from(DramaUserWatchHistory)
            .where(func.date(DramaUserWatchHistory.update_time) == today)
        )
        c_new_users_today = await db.execute(
            select(func.count()).select_from(DramaAppUser).where(func.date(DramaAppUser.create_time) == today)
        )
        sum_imp = await db.execute(select(func.coalesce(func.sum(DramaAd.impression_count), 0)))
        sum_clk = await db.execute(select(func.coalesce(func.sum(DramaAd.click_count), 0)))
        return {
            'drama_count': int(c_drama.scalar() or 0),
            'video_node_count': int(c_node.scalar() or 0),
            'pending_review_count': int(c_review.scalar() or 0),
            'pending_video_node_count': int(c_pending_nodes.scalar() or 0),
            'app_user_count': c_users,
            'today_watch_events': int(c_watch_today.scalar() or 0),
            'today_new_users': int(c_new_users_today.scalar() or 0),
            'ad_impressions_total': int(sum_imp.scalar() or 0),
            'ad_clicks_total': int(sum_clk.scalar() or 0),
        }

    # --- drama ---
    @classmethod
    async def drama_page(cls, db: AsyncSession, page_num: int, page_size: int, title: str | None = None):
        q = select(Drama).order_by(Drama.sort.desc(), Drama.drama_id.desc())
        if title:
            q = q.where(Drama.title.contains(title))
        return await PageUtil.paginate(db, q, page_num, page_size, is_page=True)

    @classmethod
    async def drama_add(cls, db: AsyncSession, m: DramaSaveModel, create_by: str) -> int:
        row = Drama(**m.model_dump(), create_by=create_by)
        db.add(row)
        await db.commit()
        await db.refresh(row)
        return row.drama_id

    @classmethod
    async def drama_edit(cls, db: AsyncSession, drama_id: int, m: DramaSaveModel, update_by: str) -> None:
        r = await db.execute(select(Drama).where(Drama.drama_id == drama_id))
        row = r.scalars().first()
        if not row:
            raise ServiceException(data='', message='短剧不存在')
        for k, v in m.model_dump().items():
            setattr(row, k, v)
        row.update_by = update_by
        row.update_time = datetime.now()
        await db.commit()

    @classmethod
    async def drama_delete(cls, db: AsyncSession, drama_id: int) -> None:
        await db.execute(delete(Drama).where(Drama.drama_id == drama_id))
        await db.commit()

    # --- video node ---
    @classmethod
    async def node_page(
        cls,
        db: AsyncSession,
        drama_id: int | None,
        page_num: int,
        page_size: int,
        review_status: str | None = None,
    ):
        q = select(DramaVideoNode).order_by(DramaVideoNode.drama_id, DramaVideoNode.sort)
        if drama_id is not None:
            q = q.where(DramaVideoNode.drama_id == drama_id)
        if review_status:
            q = q.where(DramaVideoNode.review_status == review_status)
        return await PageUtil.paginate(db, q, page_num, page_size, is_page=True)

    @classmethod
    async def node_add(cls, db: AsyncSession, m: VideoNodeSaveModel) -> int:
        row = DramaVideoNode(**m.model_dump())
        db.add(row)
        await db.commit()
        await db.refresh(row)
        return row.node_id

    @classmethod
    async def node_edit(cls, db: AsyncSession, node_id: int, m: VideoNodeSaveModel) -> None:
        r = await db.execute(select(DramaVideoNode).where(DramaVideoNode.node_id == node_id))
        row = r.scalars().first()
        if not row:
            raise ServiceException(data='', message='节点不存在')
        for k, v in m.model_dump().items():
            setattr(row, k, v)
        await db.commit()

    @classmethod
    async def node_delete(cls, db: AsyncSession, node_id: int) -> None:
        await db.execute(delete(DramaVideoChoice).where(DramaVideoChoice.node_id == node_id))
        await db.execute(delete(DramaVideoNode).where(DramaVideoNode.node_id == node_id))
        await db.commit()

    # --- choice ---
    @classmethod
    async def choice_list(cls, db: AsyncSession, node_id: int) -> list[DramaVideoChoice]:
        r = await db.execute(
            select(DramaVideoChoice)
            .where(DramaVideoChoice.node_id == node_id)
            .order_by(DramaVideoChoice.sort, DramaVideoChoice.choice_id)
        )
        return list(r.scalars().all())

    @classmethod
    async def choice_add(cls, db: AsyncSession, m: VideoChoiceSaveModel) -> int:
        row = DramaVideoChoice(**m.model_dump())
        db.add(row)
        await db.commit()
        await db.refresh(row)
        return row.choice_id

    @classmethod
    async def choice_edit(cls, db: AsyncSession, choice_id: int, m: VideoChoiceSaveModel) -> None:
        r = await db.execute(select(DramaVideoChoice).where(DramaVideoChoice.choice_id == choice_id))
        row = r.scalars().first()
        if not row:
            raise ServiceException(data='', message='选项不存在')
        for k, v in m.model_dump().items():
            setattr(row, k, v)
        await db.commit()

    @classmethod
    async def choice_delete(cls, db: AsyncSession, choice_id: int) -> None:
        await db.execute(delete(DramaVideoChoice).where(DramaVideoChoice.choice_id == choice_id))
        await db.commit()

    # --- review ---
    @classmethod
    async def review_page(cls, db: AsyncSession, status: str | None, page_num: int, page_size: int):
        q = select(DramaVideoReview).order_by(DramaVideoReview.create_time.desc())
        if status:
            q = q.where(DramaVideoReview.status == status)
        return await PageUtil.paginate(db, q, page_num, page_size, is_page=True)

    @classmethod
    async def review_audit(cls, db: AsyncSession, review_id: int, m: ReviewAuditModel) -> None:
        r = await db.execute(select(DramaVideoReview).where(DramaVideoReview.review_id == review_id))
        row = r.scalars().first()
        if not row:
            raise ServiceException(data='', message='记录不存在')
        if m.status not in ('approved', 'rejected'):
            raise ServiceException(data='', message='非法状态')
        row.status = m.status
        row.admin_remark = m.admin_remark
        row.audit_time = datetime.now()
        await db.commit()

    # --- ads ---
    @classmethod
    async def ad_page(cls, db: AsyncSession, page_num: int, page_size: int):
        q = select(DramaAd).order_by(DramaAd.weight.desc(), DramaAd.ad_id.desc())
        return await PageUtil.paginate(db, q, page_num, page_size, is_page=True)

    @classmethod
    async def ad_add(cls, db: AsyncSession, m: DramaAdSaveModel) -> int:
        data = m.model_dump()
        if not data.get('media_url') and data.get('image_url'):
            data['media_url'] = data['image_url']
        row = DramaAd(**data)
        db.add(row)
        await db.commit()
        await db.refresh(row)
        return row.ad_id

    @classmethod
    async def ad_edit(cls, db: AsyncSession, ad_id: int, m: DramaAdSaveModel) -> None:
        r = await db.execute(select(DramaAd).where(DramaAd.ad_id == ad_id))
        row = r.scalars().first()
        if not row:
            raise ServiceException(data='', message='广告不存在')
        for k, v in m.model_dump().items():
            setattr(row, k, v)
        if not row.media_url and row.image_url:
            row.media_url = row.image_url
        await db.commit()

    @classmethod
    async def ad_delete(cls, db: AsyncSession, ad_id: int) -> None:
        await db.execute(delete(DramaAd).where(DramaAd.ad_id == ad_id))
        await db.commit()

    # --- app users ---
    @classmethod
    async def app_user_page(cls, db: AsyncSession, page_num: int, page_size: int):
        q = select(DramaAppUser).order_by(DramaAppUser.create_time.desc())
        return await PageUtil.paginate(db, q, page_num, page_size, is_page=True)

    # --- upload record ---
    @classmethod
    async def create_pending_upload(
        cls,
        db: AsyncSession,
        object_key: str,
        bucket: str,
        mime: str | None,
        drama_id: int | None,
        node_id: int | None,
        create_by: str,
    ) -> int:
        row = DramaUploadFile(
            object_key=object_key,
            bucket=bucket,
            mime_type=mime,
            drama_id=drama_id,
            node_id=node_id,
            status=cls._UPP,
            create_by=create_by,
        )
        db.add(row)
        await db.commit()
        await db.refresh(row)
        return row.file_id

    @classmethod
    async def complete_upload(cls, db: AsyncSession, body: UploadCompleteIn) -> None:
        r = await db.execute(select(DramaUploadFile).where(DramaUploadFile.file_id == body.file_id))
        row = r.scalars().first()
        if not row:
            raise ServiceException(data='', message='文件记录不存在')
        row.status = 'complete'
        if body.size_bytes is not None:
            row.size_bytes = body.size_bytes

        tos_key = body.tos_key if body.tos_key else row.object_key
        video_url = body.video_url
        cover_url = body.cover_url
        if video_url is None and tos_key:
            built = DramaTosService.public_url_for_key(tos_key)
            if built:
                video_url = built

        if row.node_id:
            nr = await db.execute(select(DramaVideoNode).where(DramaVideoNode.node_id == row.node_id))
            node = nr.scalars().first()
            if node:
                if video_url:
                    node.video_url = video_url
                if cover_url:
                    node.cover_url = cover_url
                if tos_key:
                    node.tos_key = tos_key
                node.review_status = cls._RVP
                node.reject_reason = None
        await db.commit()

    @classmethod
    async def node_moderation_approve(cls, db: AsyncSession, node_id: int) -> None:
        r = await db.execute(select(DramaVideoNode).where(DramaVideoNode.node_id == node_id))
        row = r.scalars().first()
        if not row:
            raise ServiceException(data='', message='节点不存在')
        row.review_status = cls._NA
        row.reject_reason = None
        row.update_time = datetime.now()
        await db.commit()

    @classmethod
    async def node_moderation_reject(cls, db: AsyncSession, node_id: int, m: NodeModerationRejectModel) -> None:
        r = await db.execute(select(DramaVideoNode).where(DramaVideoNode.node_id == node_id))
        row = r.scalars().first()
        if not row:
            raise ServiceException(data='', message='节点不存在')
        row.review_status = cls._NR
        row.reject_reason = m.reject_reason
        row.update_time = datetime.now()
        await db.commit()

    @classmethod
    async def upload_file_page(cls, db: AsyncSession, page_num: int, page_size: int, drama_id: int | None = None):
        q = select(DramaUploadFile).order_by(DramaUploadFile.create_time.desc())
        if drama_id is not None:
            q = q.where(DramaUploadFile.drama_id == drama_id)
        return await PageUtil.paginate(db, q, page_num, page_size, is_page=True)

    @classmethod
    async def comment_page(cls, db: AsyncSession, drama_id: int | None, page_num: int, page_size: int):
        q = select(DramaComment).order_by(DramaComment.create_time.desc())
        if drama_id is not None:
            q = q.where(DramaComment.drama_id == drama_id)
        return await PageUtil.paginate(db, q, page_num, page_size, is_page=True)

    @classmethod
    async def comment_delete(cls, db: AsyncSession, comment_id: int) -> None:
        await db.execute(delete(DramaComment).where(DramaComment.comment_id == comment_id))
        await db.commit()

    @classmethod
    async def comment_hide(cls, db: AsyncSession, comment_id: int, hidden: bool = True) -> None:
        r = await db.execute(select(DramaComment).where(DramaComment.comment_id == comment_id))
        row = r.scalars().first()
        if not row:
            raise ServiceException(data='', message='评论不存在')
        row.status = '1' if hidden else '0'
        await db.commit()

    @classmethod
    async def app_user_watch_history(cls, db: AsyncSession, user_id: int) -> list[dict]:
        q = (
            select(DramaUserWatchHistory, Drama)
            .join(Drama, Drama.drama_id == DramaUserWatchHistory.drama_id)
            .where(DramaUserWatchHistory.app_user_id == user_id)
            .order_by(DramaUserWatchHistory.update_time.desc())
        )
        r = await db.execute(q)
        out = []
        for h, d in r.all():
            out.append(
                {
                    'drama_id': h.drama_id,
                    'drama_title': d.title,
                    'node_id': h.node_id,
                    'progress_sec': h.progress_sec,
                    'update_time': h.update_time,
                }
            )
        return out

    @classmethod
    async def app_user_favorites(cls, db: AsyncSession, user_id: int) -> list[dict]:
        q = (
            select(DramaUserFavorite, Drama)
            .join(Drama, Drama.drama_id == DramaUserFavorite.drama_id)
            .where(DramaUserFavorite.app_user_id == user_id)
            .order_by(DramaUserFavorite.create_time.desc())
        )
        r = await db.execute(q)
        out = []
        for f, d in r.all():
            out.append(
                {
                    'drama_id': d.drama_id,
                    'title': d.title,
                    'cover_url': d.cover_url,
                    'create_time': f.create_time,
                }
            )
        return out

    @classmethod
    async def pending_video_nodes_page(cls, db: AsyncSession, page_num: int, page_size: int):
        q = (
            select(DramaVideoNode)
            .where(DramaVideoNode.review_status == cls._RVP)
            .order_by(DramaVideoNode.create_time.desc())
        )
        return await PageUtil.paginate(db, q, page_num, page_size, is_page=True)
