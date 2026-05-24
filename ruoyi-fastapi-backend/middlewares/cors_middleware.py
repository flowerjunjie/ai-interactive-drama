from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os


def add_cors_middleware(app: FastAPI) -> None:
    """
    添加跨域中间件

    :param app: FastAPI对象
    :return:
    """
    # 前端页面url，允许通过环境变量配置，支持逗号分隔多域
    raw = os.getenv('CORS_ORIGINS', '*')
    origins = [o.strip() for o in raw.split(',')] if raw != '*' else ['*']
    expose_headers = [
        'x-body-encrypted',
        'x-key-id',
        'x-encrypt-alg',
    ]

    # 后台api允许跨域
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=bool(origins != ['*']),
        allow_methods=['*'],
        allow_headers=['*'],
        expose_headers=expose_headers,
    )
