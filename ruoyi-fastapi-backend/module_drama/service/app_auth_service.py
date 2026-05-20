from datetime import datetime, timedelta, timezone

import jwt
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from config.env import JwtConfig
from exceptions.exception import ServiceException
from module_drama.aspect.app_user_dependency import JWT_APP_TYPE
from module_drama.entity.do.drama_do import DramaAppUser
from module_drama.entity.vo.drama_vo import AppLoginModel, AppRegisterModel, AppUserBrief
from utils.pwd_util import PwdUtil


class DramaAppAuthService:
    """C 端注册/登录/JWT"""

    @classmethod
    async def register(cls, db: AsyncSession, body: AppRegisterModel) -> AppUserBrief:
        exist = await db.execute(select(DramaAppUser).where(DramaAppUser.user_name == body.user_name))
        if exist.scalars().first():
            raise ServiceException(data='', message='账号已存在')
        nick = body.nick_name or body.user_name
        user = DramaAppUser(
            user_name=body.user_name,
            nick_name=nick,
            password=PwdUtil.get_password_hash(body.password),
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return AppUserBrief(user_id=user.user_id, user_name=user.user_name, nick_name=user.nick_name, avatar=user.avatar)

    @classmethod
    async def login(cls, db: AsyncSession, body: AppLoginModel) -> str:
        r = await db.execute(select(DramaAppUser).where(DramaAppUser.user_name == body.user_name))
        user = r.scalars().first()
        if not user or not PwdUtil.verify_password(body.password, user.password):
            raise ServiceException(data='', message='用户名或密码错误')
        if user.status != '0':
            raise ServiceException(data='', message='账号已停用')
        return cls._encode_token(user.user_id)

    @classmethod
    def _encode_token(cls, user_id: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=JwtConfig.jwt_expire_minutes)
        payload = {
            'sub': str(user_id),
            'type': JWT_APP_TYPE,
            'exp': expire,
        }
        return jwt.encode(payload, JwtConfig.jwt_secret_key, algorithm=JwtConfig.jwt_algorithm)

    @classmethod
    async def me(cls, db: AsyncSession, user_id: int) -> AppUserBrief:
        r = await db.execute(select(DramaAppUser).where(DramaAppUser.user_id == user_id))
        user = r.scalars().first()
        if not user:
            raise ServiceException(data='', message='用户不存在')
        return AppUserBrief(
            user_id=user.user_id, user_name=user.user_name, nick_name=user.nick_name, avatar=user.avatar
        )

    @classmethod
    async def count_users(cls, db: AsyncSession) -> int:
        r = await db.execute(select(func.count()).select_from(DramaAppUser))
        return int(r.scalar() or 0)
