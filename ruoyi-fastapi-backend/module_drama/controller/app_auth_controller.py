from typing import Annotated

from fastapi import Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.router import APIRouterPro
from common.vo import DataResponseModel, ResponseBaseModel
from module_drama.aspect.app_user_dependency import get_required_app_user
from module_drama.entity.do.drama_do import DramaAppUser
from module_drama.entity.vo.drama_vo import AppLoginModel, AppRegisterModel, AppUserBrief
from module_drama.service.app_auth_service import DramaAppAuthService
from utils.response_util import ResponseUtil

app_auth_controller = APIRouterPro(prefix='/api/auth', order_num=40, tags=['短剧-C端认证'])


@app_auth_controller.post(
    '/register', summary='C端注册', response_model=DataResponseModel[AppUserBrief] | ResponseBaseModel
)
async def app_register(
    body: AppRegisterModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    user = await DramaAppAuthService.register(query_db, body)
    return ResponseUtil.success(msg='注册成功', data=user.model_dump())


@app_auth_controller.post('/login', summary='C端登录')
async def app_login(body: AppLoginModel, query_db: Annotated[AsyncSession, DBSessionDependency()]) -> Response:
    token = await DramaAppAuthService.login(query_db, body)
    return ResponseUtil.success(
        msg='登录成功', dict_content={'token': token, 'tokenType': 'Bearer'}  # camelCase for uni-app
    )


@app_auth_controller.get('/me', summary='当前C端用户')
async def app_me(
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current: Annotated[DramaAppUser, Depends(get_required_app_user)],
) -> Response:
    brief = await DramaAppAuthService.me(query_db, current.user_id)
    return ResponseUtil.success(data=brief.model_dump())
