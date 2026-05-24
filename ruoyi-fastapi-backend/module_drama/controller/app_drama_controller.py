from typing import Annotated
import asyncio

from fastapi import Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.annotation.rate_limit_annotation import ApiRateLimit, ApiRateLimitPreset
from common.aspect.db_seesion import DBSessionDependency
from common.router import APIRouterPro
from module_drama.aspect.app_user_dependency import get_required_app_user
from module_drama.controller.app_common_payload import choices_public, node_public
from module_drama.entity.do.drama_do import DramaAppUser
from module_drama.entity.vo.drama_vo import (
    ChoiceLogIn,
    CommentCreateModel,
    FavoriteIn,
    LikeIn,
    ReviewCreateModel,
    WatchHistoryIn,
)
from module_drama.service.drama_app_service import DramaAppContentService
from utils.response_util import ResponseUtil

app_drama_controller = APIRouterPro(prefix='/api', order_num=41, tags=['短剧-C端业务'])


@app_drama_controller.get('/feed')
@ApiRateLimit(namespace='drama:app:feed', preset=ApiRateLimitPreset.ANON_PUBLIC_METADATA)
async def feed(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    page_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
) -> Response:
    rows = await DramaAppContentService.feed(query_db, page_num, page_size)
    return ResponseUtil.success(rows=rows)


@app_drama_controller.get('/dramas')
@ApiRateLimit(namespace='drama:app:dramas', preset=ApiRateLimitPreset.ANON_PUBLIC_METADATA)
async def list_dramas(
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


@app_drama_controller.get('/dramas/{drama_id}')
@ApiRateLimit(namespace='drama:app:drama-detail', preset=ApiRateLimitPreset.ANON_PUBLIC_METADATA)
async def drama_detail(drama_id: int, query_db: Annotated[AsyncSession, DBSessionDependency()]) -> Response:
    d, entry, episodes = await asyncio.gather(
        DramaAppContentService.get_drama(query_db, drama_id),
        DramaAppContentService.entry_node(query_db, drama_id),
        DramaAppContentService.list_episodes(query_db, drama_id),
    )
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


@app_drama_controller.get('/video-nodes/{node_id}')
async def node_detail(node_id: int, query_db: Annotated[AsyncSession, DBSessionDependency()]) -> Response:
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


@app_drama_controller.get('/video-nodes/{node_id}/choices')
async def node_choices(node_id: int, query_db: Annotated[AsyncSession, DBSessionDependency()]) -> Response:
    choices = await DramaAppContentService.list_choices(query_db, node_id)
    return ResponseUtil.success(data=choices_public(choices))


async def _toggle_like_resp(
    body: LikeIn,
    query_db: AsyncSession,
    user: DramaAppUser,
) -> Response:
    state = await DramaAppContentService.toggle_like(query_db, user.user_id, body)
    return ResponseUtil.success(data=state)


@app_drama_controller.post('/likes')
async def post_like(
    body: LikeIn,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    return await _toggle_like_resp(body, query_db, user)


@app_drama_controller.post('/like')
async def post_like_alias(
    body: LikeIn,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    return await _toggle_like_resp(body, query_db, user)


@app_drama_controller.post('/watch-history')
async def post_watch_history(
    body: WatchHistoryIn,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    await DramaAppContentService.upsert_watch(query_db, user.user_id, body)
    return ResponseUtil.success(msg='已记录')


@app_drama_controller.get('/watch-history')
async def get_watch_history(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    rows = await DramaAppContentService.list_history(query_db, user.user_id)
    return ResponseUtil.success(rows=rows)


@app_drama_controller.get('/favorites')
async def get_favorites(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    rows = await DramaAppContentService.list_favorites(query_db, user.user_id)
    return ResponseUtil.success(rows=rows)


@app_drama_controller.post('/favorites')
async def post_favorite(
    body: FavoriteIn,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    state = await DramaAppContentService.toggle_favorite(query_db, user.user_id, body)
    return ResponseUtil.success(data=state)


@app_drama_controller.post('/comments')
async def post_comment(
    body: CommentCreateModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    await DramaAppContentService.add_comment(query_db, user.user_id, body)
    return ResponseUtil.success(msg='评论成功')


@app_drama_controller.get('/dramas/{drama_id}/comments')
async def get_comments_by_drama(drama_id: int, query_db: Annotated[AsyncSession, DBSessionDependency()]) -> Response:
    rows = await DramaAppContentService.list_comments(query_db, drama_id)
    return ResponseUtil.success(
        rows=[
            {'comment_id': c.comment_id, 'user_id': c.app_user_id, 'content': c.content, 'create_time': c.create_time}
            for c in rows
        ]
    )


@app_drama_controller.get('/comments')
async def get_comments_query(
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


@app_drama_controller.post('/choice-logs')
async def post_choice_log(
    body: ChoiceLogIn,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    await DramaAppContentService.log_choice(query_db, user.user_id, body)
    return ResponseUtil.success(msg='ok')


@app_drama_controller.post('/video-reviews')
async def post_review(
    body: ReviewCreateModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    user: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    await DramaAppContentService.submit_review(query_db, user.user_id, body)
    return ResponseUtil.success(msg='已提交，待审核')


@app_drama_controller.get('/ads')
@ApiRateLimit(namespace='drama:app:ads', preset=ApiRateLimitPreset.ANON_PUBLIC_METADATA)
async def list_ads(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    slot: str | None = Query(default=None),
) -> Response:
    rows = await DramaAppContentService.list_ads(query_db, slot)
    return ResponseUtil.success(rows=[DramaAppContentService._ad_public_dict(a) for a in rows])


@app_drama_controller.post('/ads/{ad_id}/impression')
async def ad_impression(ad_id: int, query_db: Annotated[AsyncSession, DBSessionDependency()]) -> Response:
    await DramaAppContentService.ad_impression(query_db, ad_id)
    return ResponseUtil.success(msg='ok')


@app_drama_controller.post('/ads/{ad_id}/click')
async def ad_click(ad_id: int, query_db: Annotated[AsyncSession, DBSessionDependency()]) -> Response:
    await DramaAppContentService.ad_click(query_db, ad_id)
    return ResponseUtil.success(msg='ok')
