from typing import Annotated

from fastapi import Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.annotation.rate_limit_annotation import ApiRateLimit, ApiRateLimitPreset
from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.constant import CommonConstant
from common.router import APIRouterPro
from config.env import TosConfig
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_drama.entity.vo.drama_vo import (
    DramaAdSaveModel,
    DramaSaveModel,
    NodeModerationRejectModel,
    ReviewAuditModel,
    UploadCompleteIn,
    VideoChoiceSaveModel,
    VideoNodeSaveModel,
)
from module_drama.service.drama_admin_service import DramaAdminService
from module_drama.service.tos_service import DramaTosService
from utils.response_util import ResponseUtil

admin_drama_controller = APIRouterPro(
    prefix='/api/admin/drama',
    order_num=42,
    tags=['短剧-后台管理'],
    dependencies=[PreAuthDependency()],
)


@admin_drama_controller.get(
    '/dashboard', summary='数据看板', dependencies=[UserInterfaceAuthDependency('sdrama:dashboard:view')]
)
async def dashboard(query_db: Annotated[AsyncSession, DBSessionDependency()]) -> Response:
    data = await DramaAdminService.dashboard(query_db)
    return ResponseUtil.success(data=data)


# --- drama CRUD ---
@admin_drama_controller.get('/dramas', dependencies=[UserInterfaceAuthDependency('sdrama:drama:list')])
async def admin_drama_list(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    page_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    title: str | None = Query(default=None),
) -> Response:
    page = await DramaAdminService.drama_page(query_db, page_num, page_size, title)
    return ResponseUtil.success(model_content=page)


@admin_drama_controller.post('/dramas', dependencies=[UserInterfaceAuthDependency('sdrama:drama:add')])
@ApiRateLimit(namespace='drama:admin:drama', preset=ApiRateLimitPreset.USER_COMMON_MUTATION)
async def admin_drama_add(
    body: DramaSaveModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    cu: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    uid = await DramaAdminService.drama_add(query_db, body, cu.user.user_name if cu.user else 'admin')
    return ResponseUtil.success(msg='新增成功', data={'dramaId': uid})


@admin_drama_controller.put('/dramas/{drama_id}', dependencies=[UserInterfaceAuthDependency('sdrama:drama:edit')])
@ApiRateLimit(namespace='drama:admin:drama', preset=ApiRateLimitPreset.USER_COMMON_MUTATION)
async def admin_drama_edit(
    drama_id: int,
    body: DramaSaveModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    cu: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    await DramaAdminService.drama_edit(query_db, drama_id, body, cu.user.user_name if cu.user else 'admin')
    return ResponseUtil.success(msg='更新成功')


@admin_drama_controller.delete('/dramas/{drama_id}', dependencies=[UserInterfaceAuthDependency('sdrama:drama:remove')])
async def admin_drama_del(
    drama_id: int,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    await DramaAdminService.drama_delete(query_db, drama_id)
    return ResponseUtil.success(msg='删除成功')


# --- nodes ---
@admin_drama_controller.get('/video-nodes', dependencies=[UserInterfaceAuthDependency('sdrama:node:list')])
async def admin_node_list(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    drama_id: int | None = Query(default=None),
    review_status: str | None = Query(default=None),
    page_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
) -> Response:
    page = await DramaAdminService.node_page(query_db, drama_id, page_num, page_size, review_status)
    return ResponseUtil.success(model_content=page)


@admin_drama_controller.post('/video-nodes', dependencies=[UserInterfaceAuthDependency('sdrama:node:add')])
@ApiRateLimit(namespace='drama:admin:node', preset=ApiRateLimitPreset.USER_COMMON_MUTATION)
async def admin_node_add(
    body: VideoNodeSaveModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    nid = await DramaAdminService.node_add(query_db, body)
    return ResponseUtil.success(msg='新增成功', data={'nodeId': nid})


@admin_drama_controller.put('/video-nodes/{node_id}', dependencies=[UserInterfaceAuthDependency('sdrama:node:edit')])
@ApiRateLimit(namespace='drama:admin:node', preset=ApiRateLimitPreset.USER_COMMON_MUTATION)
async def admin_node_edit(
    node_id: int,
    body: VideoNodeSaveModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    await DramaAdminService.node_edit(query_db, node_id, body)
    return ResponseUtil.success(msg='更新成功')


@admin_drama_controller.delete(
    '/video-nodes/{node_id}', dependencies=[UserInterfaceAuthDependency('sdrama:node:remove')]
)
async def admin_node_del(
    node_id: int,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    await DramaAdminService.node_delete(query_db, node_id)
    return ResponseUtil.success(msg='删除成功')


@admin_drama_controller.put(
    '/video-nodes/{node_id}/moderation/approve',
    dependencies=[UserInterfaceAuthDependency('sdrama:node:edit')],
)
async def admin_node_moderation_approve(
    node_id: int, query_db: Annotated[AsyncSession, DBSessionDependency()]
) -> Response:
    await DramaAdminService.node_moderation_approve(query_db, node_id)
    return ResponseUtil.success(msg='已通过')


@admin_drama_controller.put(
    '/video-nodes/{node_id}/moderation/reject',
    dependencies=[UserInterfaceAuthDependency('sdrama:node:edit')],
)
async def admin_node_moderation_reject(
    node_id: int,
    body: NodeModerationRejectModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    await DramaAdminService.node_moderation_reject(query_db, node_id, body)
    return ResponseUtil.success(msg='已拒绝')


@admin_drama_controller.get(
    '/video-nodes/pending-moderation', dependencies=[UserInterfaceAuthDependency('sdrama:node:list')]
)
async def admin_pending_video_nodes(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    page_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
) -> Response:
    page = await DramaAdminService.pending_video_nodes_page(query_db, page_num, page_size)
    return ResponseUtil.success(model_content=page)


@admin_drama_controller.get('/upload-files', dependencies=[UserInterfaceAuthDependency('sdrama:node:list')])
async def admin_upload_files(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    page_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    drama_id: int | None = Query(default=None),
) -> Response:
    page = await DramaAdminService.upload_file_page(query_db, page_num, page_size, drama_id)
    return ResponseUtil.success(model_content=page)


@admin_drama_controller.get('/comments', dependencies=[UserInterfaceAuthDependency('sdrama:drama:list')])
async def admin_comments(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    page_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    drama_id: int | None = Query(default=None),
) -> Response:
    page = await DramaAdminService.comment_page(query_db, drama_id, page_num, page_size)
    return ResponseUtil.success(model_content=page)


@admin_drama_controller.delete(
    '/comments/{comment_id}', dependencies=[UserInterfaceAuthDependency('sdrama:drama:list')]
)
async def admin_comment_delete(comment_id: int, query_db: Annotated[AsyncSession, DBSessionDependency()]) -> Response:
    await DramaAdminService.comment_delete(query_db, comment_id)
    return ResponseUtil.success(msg='已删除')


@admin_drama_controller.put(
    '/comments/{comment_id}/hide', dependencies=[UserInterfaceAuthDependency('sdrama:drama:list')]
)
async def admin_comment_hide(
    comment_id: int,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    hidden: bool = Query(default=True),
) -> Response:
    await DramaAdminService.comment_hide(query_db, comment_id, hidden)
    return ResponseUtil.success(msg='已更新')


@admin_drama_controller.get(
    '/app-users/{user_id}/watch-history',
    dependencies=[UserInterfaceAuthDependency('sdrama:appuser:list')],
)
async def admin_app_user_watch(user_id: int, query_db: Annotated[AsyncSession, DBSessionDependency()]) -> Response:
    rows = await DramaAdminService.app_user_watch_history(query_db, user_id)
    return ResponseUtil.success(rows=rows)


@admin_drama_controller.get(
    '/app-users/{user_id}/favorites',
    dependencies=[UserInterfaceAuthDependency('sdrama:appuser:list')],
)
async def admin_app_user_favs(user_id: int, query_db: Annotated[AsyncSession, DBSessionDependency()]) -> Response:
    rows = await DramaAdminService.app_user_favorites(query_db, user_id)
    return ResponseUtil.success(rows=rows)


# --- choices ---
@admin_drama_controller.get(
    '/video-nodes/{node_id}/choices', dependencies=[UserInterfaceAuthDependency('sdrama:choice:list')]
)
async def admin_choice_list(node_id: int, query_db: Annotated[AsyncSession, DBSessionDependency()]) -> Response:
    rows = await DramaAdminService.choice_list(query_db, node_id)
    return ResponseUtil.success(
        rows=[
            {
                'choiceId': c.choice_id,
                'choiceCode': c.choice_code,
                'label': c.label,
                'nextNodeId': c.next_node_id,
                'sort': c.sort,
            }
            for c in rows
        ]
    )


@admin_drama_controller.post('/video-choices', dependencies=[UserInterfaceAuthDependency('sdrama:choice:add')])
async def admin_choice_add(
    body: VideoChoiceSaveModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    cid = await DramaAdminService.choice_add(query_db, body)
    return ResponseUtil.success(data={'choiceId': cid})


@admin_drama_controller.put(
    '/video-choices/{choice_id}', dependencies=[UserInterfaceAuthDependency('sdrama:choice:edit')]
)
async def admin_choice_edit(
    choice_id: int,
    body: VideoChoiceSaveModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    await DramaAdminService.choice_edit(query_db, choice_id, body)
    return ResponseUtil.success(msg='更新成功')


@admin_drama_controller.delete(
    '/video-choices/{choice_id}', dependencies=[UserInterfaceAuthDependency('sdrama:choice:remove')]
)
async def admin_choice_del(
    choice_id: int,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    await DramaAdminService.choice_delete(query_db, choice_id)
    return ResponseUtil.success(msg='删除成功')


# --- reviews ---
@admin_drama_controller.get('/video-reviews', dependencies=[UserInterfaceAuthDependency('sdrama:review:list')])
async def admin_review_list(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    status: str | None = Query(default=CommonConstant.DRAMA_REVIEW_STATUS_PENDING),
    page_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
) -> Response:
    page = await DramaAdminService.review_page(query_db, status, page_num, page_size)
    return ResponseUtil.success(model_content=page)


@admin_drama_controller.put(
    '/video-reviews/{review_id}/audit', dependencies=[UserInterfaceAuthDependency('sdrama:review:audit')]
)
async def admin_review_audit(
    review_id: int,
    body: ReviewAuditModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    await DramaAdminService.review_audit(query_db, review_id, body)
    return ResponseUtil.success(msg='已处理')


# --- ads ---
@admin_drama_controller.get('/ads', dependencies=[UserInterfaceAuthDependency('sdrama:ad:list')])
async def admin_ad_list(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    page_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
) -> Response:
    page = await DramaAdminService.ad_page(query_db, page_num, page_size)
    return ResponseUtil.success(model_content=page)


@admin_drama_controller.post('/ads', dependencies=[UserInterfaceAuthDependency('sdrama:ad:add')])
async def admin_ad_add(
    body: DramaAdSaveModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    aid = await DramaAdminService.ad_add(query_db, body)
    return ResponseUtil.success(data={'adId': aid})


@admin_drama_controller.put('/ads/{ad_id}', dependencies=[UserInterfaceAuthDependency('sdrama:ad:edit')])
async def admin_ad_edit(
    ad_id: int,
    body: DramaAdSaveModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    await DramaAdminService.ad_edit(query_db, ad_id, body)
    return ResponseUtil.success(msg='更新成功')


@admin_drama_controller.delete('/ads/{ad_id}', dependencies=[UserInterfaceAuthDependency('sdrama:ad:remove')])
async def admin_ad_del(
    ad_id: int,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    await DramaAdminService.ad_delete(query_db, ad_id)
    return ResponseUtil.success(msg='删除成功')


# --- app users ---
@admin_drama_controller.get('/app-users', dependencies=[UserInterfaceAuthDependency('sdrama:appuser:list')])
async def admin_app_users(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    page_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
) -> Response:
    page = await DramaAdminService.app_user_page(query_db, page_num, page_size)
    return ResponseUtil.success(model_content=page)


# --- upload ---
@admin_drama_controller.get('/upload/sign', dependencies=[UserInterfaceAuthDependency('sdrama:upload:sign')])
async def admin_upload_sign(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    cu: Annotated[CurrentUserModel, CurrentUserDependency()],
    filename: str = Query(..., min_length=1, max_length=255),
    content_type: str = Query(default='video/mp4', max_length=128),
    drama_id: int | None = Query(default=None),
    node_id: int | None = Query(default=None),
    object_kind: str | None = Query(default=None, description='videos/covers/ads 使用规格路径'),
) -> Response:
    if object_kind in ('videos', 'covers', 'ads'):
        key = DramaTosService.build_object_key_spec(object_kind, filename)
    else:
        key = DramaTosService.build_object_key_legacy(drama_id, node_id, filename)
    url = DramaTosService.presign_put(key, content_type)
    fid = await DramaAdminService.create_pending_upload(
        query_db,
        key,
        TosConfig.volcengine_tos_bucket,
        content_type,
        drama_id,
        node_id,
        cu.user.user_name if cu.user else 'admin',
    )
    return ResponseUtil.success(
        data={'uploadUrl': url, 'objectKey': key, 'bucket': TosConfig.volcengine_tos_bucket, 'fileId': fid}
    )


@admin_drama_controller.post('/upload/complete', dependencies=[UserInterfaceAuthDependency('sdrama:upload:complete')])
async def admin_upload_complete(
    body: UploadCompleteIn,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    await DramaAdminService.complete_upload(query_db, body)
    return ResponseUtil.success(msg='已完成')
