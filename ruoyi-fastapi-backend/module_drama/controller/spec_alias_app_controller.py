"""规格文档路径 /api/app/*（与 /api/* 并存）"""

from typing import Annotated

from fastapi import Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.annotation.rate_limit_annotation import ApiRateLimit, ApiRateLimitPreset
from common.annotation.rate_limit_annotation import ApiRateLimit, ApiRateLimitPreset
from common.aspect.db_seesion import DBSessionDependency
from common.constant import ApiNamespace
from common.router import APIRouterPro
from module_drama.aspect.app_user_dependency import get_optional_app_user, get_required_app_user
from module_drama.controller.app_common_payload import choices_public, node_public
from module_drama.entity.do.drama_do import DramaAppUser
from module_drama.entity.vo.drama_vo import (
    ChoiceLogIn,
    CommentCreateModel,
    FavoriteIn,
    LikeIn,
    SubscribeIn,
    WatchHistoryIn,
)
from module_drama.service.drama_app_service import DramaAppContentService
from utils.response_util import ResponseUtil

spec_app_controller = APIRouterPro(prefix='/api/app', order_num=38, tags=['短剧-C端规格路径'])


@spec_app_controller.get('/me/dashboard')
async def spec_me_dashboard(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    data = await DramaAppContentService.user_dashboard_counts(query_db, user.user_id)
    return ResponseUtil.success(data=data)


@spec_app_controller.get('/feed')
@ApiRateLimit(namespace='drama:app:feed', preset=ApiRateLimitPreset.ANON_PUBLIC_METADATA)
async def spec_feed(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    page_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
) -> Response:
    rows = await DramaAppContentService.feed(query_db, page_num, page_size)
    return ResponseUtil.success(rows=rows)


@spec_app_controller.get('/dramas/{drama_id}/favorite-state')
async def spec_drama_favorite_state(
    drama_id: int,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser | None, Depends(get_optional_app_user)],
) -> Response:
    if user is None:
        return ResponseUtil.success(data={'favorited': False})
    ok = await DramaAppContentService.is_drama_favorited(query_db, user.user_id, drama_id)
    return ResponseUtil.success(data={'favorited': ok})


@spec_app_controller.get('/video-nodes/{node_id}/me-like')
async def spec_node_me_like(
    node_id: int,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser | None, Depends(get_optional_app_user)],
) -> Response:
    if user is None:
        return ResponseUtil.success(data={'liked': False})
    ok = await DramaAppContentService.user_has_liked(query_db, user.user_id, 'node', node_id)
    return ResponseUtil.success(data={'liked': ok})


@spec_app_controller.get('/dramas')
@ApiRateLimit(namespace='drama:app:dramas', preset=ApiRateLimitPreset.ANON_PUBLIC_METADATA)
async def spec_dramas(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    drama_type: str | None = Query(default=None),
    keyword: str | None = Query(default=None),
    sort: str | None = Query(default=None, description='recommend|latest|heat'),
    page_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=50),
) -> Response:
    rows, total = await DramaAppContentService.list_dramas(query_db, drama_type, keyword, sort, page_num, page_size)
    return ResponseUtil.success(
        rows=[
            {
                'drama_id': d.drama_id,
                'title': d.title,
                'cover_url': d.cover_url,
                'description': d.description,
                'drama_type': d.drama_type,
                'tags': d.tags,
                'heat': d.heat,
            }
            for d in rows
        ],
        dict_content={'total': total},
    )


@spec_app_controller.get('/dramas/{drama_id}')
@ApiRateLimit(namespace='drama:app:drama-detail', preset=ApiRateLimitPreset.ANON_PUBLIC_METADATA)
async def spec_drama_detail(drama_id: int, query_db: Annotated[AsyncSession, DBSessionDependency()]) -> Response:
    d = await DramaAppContentService.get_drama(query_db, drama_id)
    entry = await DramaAppContentService.entry_node(query_db, drama_id)
    episodes = await DramaAppContentService.list_episodes(query_db, drama_id)
    return ResponseUtil.success(
        data={
            'drama': {
                'drama_id': d.drama_id,
                'title': d.title,
                'cover_url': d.cover_url,
                'description': d.description,
                'drama_type': d.drama_type,
                'tags': d.tags,
                'heat': d.heat,
            },
            'entry_node_id': entry.node_id if entry else None,
            'episodes': [node_public(n) for n in episodes],
            'episode_total': len(episodes),
        }
    )


@spec_app_controller.get('/video-nodes/{node_id}')
async def spec_node_detail(node_id: int, query_db: Annotated[AsyncSession, DBSessionDependency()]) -> Response:
    n = await DramaAppContentService.get_node(query_db, node_id)
    choices = await DramaAppContentService.list_choices(query_db, node_id)
    likes = await DramaAppContentService.like_count(query_db, 'node', node_id)
    return ResponseUtil.success(
        data={
            'node': node_public(n),
            'choices': choices_public(choices),
            'like_count': likes,
        }
    )


@spec_app_controller.get('/video-nodes/{node_id}/choices')
async def spec_node_choices(node_id: int, query_db: Annotated[AsyncSession, DBSessionDependency()]) -> Response:
    choices = await DramaAppContentService.list_choices(query_db, node_id)
    return ResponseUtil.success(data=choices_public(choices))


@spec_app_controller.post('/watch-history')
async def spec_watch_post(
    body: WatchHistoryIn,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    await DramaAppContentService.upsert_watch(query_db, user.user_id, body)
    return ResponseUtil.success(msg='已记录')


@spec_app_controller.get('/watch-history')
async def spec_watch_get(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    rows = await DramaAppContentService.list_history(query_db, user.user_id)
    return ResponseUtil.success(rows=rows)


@spec_app_controller.post('/like')
async def spec_like(
    body: LikeIn,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    state = await DramaAppContentService.toggle_like(query_db, user.user_id, body)
    return ResponseUtil.success(data=state)


async def _spec_toggle_favorite(
    body: FavoriteIn,
    query_db: AsyncSession,
    user: DramaAppUser,
) -> Response:
    state = await DramaAppContentService.toggle_favorite(query_db, user.user_id, body)
    return ResponseUtil.success(data=state)


@spec_app_controller.post('/favorite')
async def spec_favorite_singular(
    body: FavoriteIn,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    return await _spec_toggle_favorite(body, query_db, user)


@spec_app_controller.get('/favorites')
async def spec_favorites_get(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    rows = await DramaAppContentService.list_favorites(query_db, user.user_id)
    return ResponseUtil.success(rows=rows)


@spec_app_controller.post('/favorites')
async def spec_favorites_plural(
    body: FavoriteIn,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    return await _spec_toggle_favorite(body, query_db, user)


@spec_app_controller.post('/comments')
async def spec_comment_post(
    body: CommentCreateModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    await DramaAppContentService.add_comment(query_db, user.user_id, body)
    return ResponseUtil.success(msg='评论成功')


@spec_app_controller.get('/comments')
async def spec_comments_get(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    drama_id: int = Query(..., ge=1),
) -> Response:
    rows = await DramaAppContentService.list_comments(query_db, drama_id)
    return ResponseUtil.success(
        rows=[
            {'comment_id': c.comment_id, 'user_id': c.app_user_id, 'content': c.content, 'create_time': c.create_time}
            for c in rows
        ]
    )


@spec_app_controller.post('/choice-logs')
async def spec_choice_log(
    body: ChoiceLogIn,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    await DramaAppContentService.log_choice(query_db, user.user_id, body)
    return ResponseUtil.success(msg='ok')


@spec_app_controller.get('/ads')
async def spec_ads(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    slot: str | None = Query(default=None),
) -> Response:
    rows = await DramaAppContentService.list_ads(query_db, slot)
    return ResponseUtil.success(rows=[DramaAppContentService._ad_public_dict(a) for a in rows])


@spec_app_controller.post('/ads/{ad_id}/impression')
async def spec_ad_imp(ad_id: int, query_db: Annotated[AsyncSession, DBSessionDependency()]) -> Response:
    await DramaAppContentService.ad_impression(query_db, ad_id)
    return ResponseUtil.success(msg='ok')


@spec_app_controller.post('/ads/{ad_id}/click')
async def spec_ad_click(ad_id: int, query_db: Annotated[AsyncSession, DBSessionDependency()]) -> Response:
    await DramaAppContentService.ad_click(query_db, ad_id)
    return ResponseUtil.success(msg='ok')


@spec_app_controller.post('/subscriptions')
async def spec_subscribe(
    body: SubscribeIn,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    state = await DramaAppContentService.toggle_subscribe(query_db, user.user_id, body.drama_id, body.notify_enabled)
    return ResponseUtil.success(data=state)


@spec_app_controller.get('/subscriptions')
async def spec_subscriptions_get(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    rows = await DramaAppContentService.list_subscriptions(query_db, user.user_id)
    return ResponseUtil.success(rows=rows)


@spec_app_controller.get('/subscriptions/{drama_id}/new-episode')
async def spec_subscribe_check(
    drama_id: int,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    result = await DramaAppContentService.check_new_episodes(query_db, user.user_id, drama_id)
    return ResponseUtil.success(data=result)
