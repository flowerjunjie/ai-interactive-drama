from typing import Annotated

import jwt
from fastapi import Depends
from fastapi import params
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from config.env import JwtConfig
from exceptions.exception import AuthException
from module_drama.entity.do.drama_do import DramaAppUser

_app_bearer = HTTPBearer(auto_error=False)

JWT_APP_TYPE = 'drama_app'


async def get_optional_app_user(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(_app_bearer)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> DramaAppUser | None:
    """解析 Bearer JWT（C 端），失败时不抛错。"""
    if not creds or not creds.credentials:
        return None
    token = creds.credentials
    try:
        payload = jwt.decode(token, JwtConfig.jwt_secret_key, algorithms=[JwtConfig.jwt_algorithm])
    except (InvalidTokenError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
    if payload.get('typ') != JWT_APP_TYPE:
        return None
    uid = payload.get('sub')
    if not uid:
        return None
    result = await query_db.execute(select(DramaAppUser).where(DramaAppUser.user_id == int(uid)))
    user = result.scalars().first()
    if not user or user.status != '0':
        return None
    return user


async def get_required_app_user(
    user: Annotated[DramaAppUser | None, Depends(get_optional_app_user)],
) -> DramaAppUser:
    if user is None:
        raise AuthException(data='', message='请先登录 C 端账号')
    return user


def CurrentAppUserDependency() -> params.Depends:
    return Depends(get_required_app_user)


def OptionalAppUserDependency() -> params.Depends:
    return Depends(get_optional_app_user)
