"""规格文档后台路径：/api/admin/upload/*、/reviews/*、顶层 dramas/video-nodes（与 /api/admin/drama/* 并存）"""

from typing import Annotated

from fastapi import Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.router import APIRouterPro
from config.env import TosConfig
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_drama.entity.vo.drama_vo import NodeModerationRejectModel, UploadCompleteIn
from module_drama.service.drama_admin_service import DramaAdminService
from module_drama.service.tos_service import DramaTosService
from utils.response_util import ResponseUtil

spec_admin_alias_controller = APIRouterPro(
    prefix='/api/admin',
    order_num=43,
    tags=['短剧-规格后台别名'],
    dependencies=[PreAuthDependency()],
)


@spec_admin_alias_controller.post('/upload/sign', dependencies=[UserInterfaceAuthDependency('sdrama:upload:sign')])
async def spec_admin_upload_sign_post(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    cu: Annotated[CurrentUserModel, CurrentUserDependency()],
    filename: str = Query(..., min_length=1, max_length=255),
    content_type: str = Query(default='video/mp4', max_length=128),
    drama_id: int | None = Query(default=None),
    node_id: int | None = Query(default=None),
    object_kind: str | None = Query(default=None, description='videos/covers/ads'),
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
        data={'uploadUrl': url, 'upload_url': url, 'objectKey': key, 'object_key': key, 'bucket': TosConfig.volcengine_tos_bucket, 'fileId': fid}
    )


@spec_admin_alias_controller.post('/upload/complete', dependencies=[UserInterfaceAuthDependency('sdrama:upload:complete')])
async def spec_admin_upload_complete_post(
    body: UploadCompleteIn,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    await DramaAdminService.complete_upload(query_db, body)
    return ResponseUtil.success(msg='已完成')


@spec_admin_alias_controller.get('/dramas', dependencies=[UserInterfaceAuthDependency('sdrama:drama:list')])
async def spec_admin_dramas(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    page_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    title: str | None = Query(default=None),
) -> Response:
    page = await DramaAdminService.drama_page(query_db, page_num, page_size, title)
    return ResponseUtil.success(model_content=page)


@spec_admin_alias_controller.get('/video-nodes', dependencies=[UserInterfaceAuthDependency('sdrama:node:list')])
async def spec_admin_video_nodes(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    drama_id: int | None = Query(default=None),
    review_status: str | None = Query(default=None),
    page_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
) -> Response:
    page = await DramaAdminService.node_page(query_db, drama_id, page_num, page_size, review_status)
    return ResponseUtil.success(model_content=page)


@spec_admin_alias_controller.get('/reviews/pending', dependencies=[UserInterfaceAuthDependency('sdrama:node:list')])
async def spec_reviews_pending(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    page_num: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
) -> Response:
    page = await DramaAdminService.pending_video_nodes_page(query_db, page_num, page_size)
    return ResponseUtil.success(model_content=page)


@spec_admin_alias_controller.post(
    '/reviews/{node_id}/approve',
    dependencies=[UserInterfaceAuthDependency('sdrama:node:edit')],
)
async def spec_review_approve(node_id: int, query_db: Annotated[AsyncSession, DBSessionDependency()]) -> Response:
    await DramaAdminService.node_moderation_approve(query_db, node_id)
    return ResponseUtil.success(msg='已通过')


@spec_admin_alias_controller.post(
    '/reviews/{node_id}/reject',
    dependencies=[UserInterfaceAuthDependency('sdrama:node:edit')],
)
async def spec_review_reject(
    node_id: int,
    body: NodeModerationRejectModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    await DramaAdminService.node_moderation_reject(query_db, node_id, body)
    return ResponseUtil.success(msg='已拒绝')
