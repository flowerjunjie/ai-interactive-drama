import uuid
from datetime import datetime

import tos
from tos.enum import HttpMethodType

from config.env import TosConfig
from exceptions.exception import ServiceException


class DramaTosService:
    """TOS 预签名 PUT（前端直传）"""

    @classmethod
    def _client(cls) -> tos.TosClientV2:
        if not all(
            [
                TosConfig.volcengine_tos_access_key,
                TosConfig.volcengine_tos_secret_key,
                TosConfig.volcengine_tos_bucket,
                TosConfig.volcengine_tos_endpoint,
            ]
        ):
            raise ServiceException(data='', message='未配置 VOLCENGINE_TOS_ACCESS_KEY / SECRET_KEY / BUCKET / ENDPOINT')
        return tos.TosClientV2(
            TosConfig.volcengine_tos_access_key,
            TosConfig.volcengine_tos_secret_key,
            TosConfig.volcengine_tos_endpoint,
            TosConfig.volcengine_tos_region,
        )

    @classmethod
    def build_object_key_legacy(cls, drama_id: int | None, node_id: int | None, filename: str) -> str:
        """兼容旧路径：dramas/{id}/nodes/{nid}/upload/{uuid}_{name}"""
        safe_name = filename.replace('..', '').replace('\\', '/').split('/')[-1]
        uid = uuid.uuid4().hex[:12]
        parts = ['dramas', str(drama_id or 0), 'nodes', str(node_id or 0), 'upload', f'{uid}_{safe_name}']
        return '/'.join(parts)

    @classmethod
    def build_object_key_spec(cls, kind: str, filename: str) -> str:
        """规格路径：videos|covers|ads/{yyyyMMdd}/{uuid}.保留后缀"""
        safe_name = filename.replace('..', '').replace('\\', '/').split('/')[-1]
        dot = safe_name.rfind('.')
        ext = safe_name[dot:] if dot > 0 else ''
        uid = uuid.uuid4().hex
        day = datetime.now().strftime('%Y%m%d')
        prefix = kind.strip().lower()
        if prefix not in ('videos', 'covers', 'ads'):
            raise ServiceException(data='', message='object_kind 须为 videos / covers / ads')
        return f'{prefix}/{day}/{uid}{ext}'

    @classmethod
    def public_url_for_key(cls, object_key: str) -> str | None:
        """用 CDN 域名拼接访问 URL；未配置则返回 None"""
        base = (TosConfig.volcengine_tos_cdn_domain or '').strip().rstrip('/')
        if not base:
            return None
        key = object_key.lstrip('/')
        return f'{base}/{key}'

    @classmethod
    def presign_put(cls, object_key: str, content_type: str | None) -> str:
        client = cls._client()
        header = {}
        if content_type:
            header['Content-Type'] = content_type
        out = client.pre_signed_url(
            HttpMethodType.Http_Method_Put,
            TosConfig.volcengine_tos_bucket,
            object_key,
            expires=TosConfig.volcengine_tos_presign_expires,
            header=header or None,
        )
        if hasattr(out, 'signed_url'):
            return out.signed_url
        if isinstance(out, str):
            return out
        return str(out)
