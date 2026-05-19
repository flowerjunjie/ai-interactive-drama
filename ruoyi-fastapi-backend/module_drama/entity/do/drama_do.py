"""
短剧平台业务表（MVP）
"""

from datetime import datetime

from sqlalchemy import (
    CHAR,
    BigInteger,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

from config.database import Base
from config.env import DataBaseConfig
from utils.common_util import SqlalchemyUtil


class DramaAppUser(Base):
    """C 端应用用户"""

    __tablename__ = 'drama_app_user'
    __table_args__ = {'comment': '短剧 C 端用户'}

    user_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='用户ID')
    user_name = Column(String(64), nullable=False, unique=True, comment='登录账号')
    nick_name = Column(String(64), nullable=False, comment='昵称')
    password = Column(String(100), nullable=False, comment='密码hash')
    avatar = Column(String(512), nullable=True, server_default="''", comment='头像 URL')
    status = Column(CHAR(1), nullable=False, server_default='0', comment='0正常 1停用')
    create_time = Column(DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_time = Column(DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='更新时间')


class Drama(Base):
    """短剧元信息"""

    __tablename__ = 'drama'
    __table_args__ = {'comment': '短剧'}

    drama_id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, comment='标题')
    cover_url = Column(String(1024), nullable=True, comment='封面')
    description = Column(Text, nullable=True, comment='简介')
    drama_type = Column(
        String(32), nullable=False, server_default='comic_drama', comment='comic_drama / live_action'
    )
    status = Column(
        String(32), nullable=False, server_default='draft', comment='draft / published / offline'
    )
    sort = Column(Integer, nullable=False, server_default='0', comment='排序')
    create_by = Column(String(64), nullable=True, server_default="''", comment='创建者')
    create_time = Column(DateTime, nullable=True, default=datetime.now, comment='创建时间')
    update_by = Column(String(64), nullable=True, server_default="''", comment='更新者')
    update_time = Column(DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    remark = Column(
        String(500),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='备注',
    )
    tags = Column(String(512), nullable=True, comment='标签 JSON 或逗号分隔')
    heat = Column(Integer, nullable=False, server_default='0', comment='热度')


class DramaVideoNode(Base):
    """剧情节点（垂直流 / 树）"""

    __tablename__ = 'drama_video_node'
    __table_args__ = {'comment': '剧情视频节点'}

    node_id = Column(BigInteger, primary_key=True, autoincrement=True)
    drama_id = Column(BigInteger, nullable=False, comment='短剧 ID')
    parent_node_id = Column(BigInteger, nullable=True, comment='父节点')
    title = Column(String(200), nullable=True, comment='节点标题')
    video_url = Column(String(1024), nullable=True, comment='视频地址')
    cover_url = Column(String(1024), nullable=True, comment='封面')
    tos_key = Column(String(512), nullable=True, comment='TOS 对象键')
    duration_sec = Column(Integer, nullable=True, comment='时长秒')
    episode_no = Column(Integer, nullable=True, comment='集序号')
    sort = Column(Integer, nullable=False, server_default='0')
    is_entry = Column(CHAR(1), nullable=False, server_default='0', comment='是否入口节点 0否 1是')
    is_interactive = Column(CHAR(1), nullable=False, server_default='0', comment='互动节点 0否 1是')
    choice_trigger_sec = Column(Float, nullable=True, comment='分支弹出时刻(秒)')
    status = Column(String(32), nullable=False, server_default='draft', comment='draft / published / offline')
    review_status = Column(
        String(32), nullable=False, server_default='pending', comment='pending / approved / rejected'
    )
    reject_reason = Column(String(500), nullable=True, comment='审核拒绝原因')
    create_time = Column(DateTime, nullable=True, default=datetime.now)
    update_time = Column(DateTime, nullable=True, default=datetime.now, onupdate=datetime.now)


class DramaVideoChoice(Base):
    """分支选项"""

    __tablename__ = 'drama_video_choice'
    __table_args__ = {'comment': '分支选项'}

    choice_id = Column(BigInteger, primary_key=True, autoincrement=True)
    node_id = Column(BigInteger, nullable=False, comment='所属节点')
    choice_code = Column(String(8), nullable=True, comment='选项编码 A/B/C')
    label = Column(String(200), nullable=False, comment='选项文案')
    next_node_id = Column(BigInteger, nullable=False, comment='跳转节点')
    sort = Column(Integer, nullable=False, server_default='0')
    create_time = Column(DateTime, nullable=True, default=datetime.now)


class DramaVideoReview(Base):
    """用户评价（需审核）"""

    __tablename__ = 'drama_video_review'
    __table_args__ = {'comment': '用户评价审核'}

    review_id = Column(BigInteger, primary_key=True, autoincrement=True)
    app_user_id = Column(BigInteger, nullable=False)
    drama_id = Column(BigInteger, nullable=False)
    node_id = Column(BigInteger, nullable=True)
    rating = Column(Integer, nullable=True, comment='1-5')
    content = Column(Text, nullable=True)
    status = Column(
        String(32), nullable=False, server_default='pending', comment='pending / approved / rejected'
    )
    admin_remark = Column(String(500), nullable=True)
    create_time = Column(DateTime, nullable=True, default=datetime.now)
    audit_time = Column(DateTime, nullable=True)


class DramaAd(Base):
    """广告位"""

    __tablename__ = 'drama_ad'
    __table_args__ = {'comment': '短剧广告'}

    ad_id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    media_type = Column(String(16), nullable=False, server_default='image', comment='image / video')
    media_url = Column(String(1024), nullable=True, comment='主素材 URL')
    image_url = Column(String(1024), nullable=True, comment='兼容旧字段')
    cover_url = Column(String(1024), nullable=True, comment='视频封面')
    link_url = Column(String(1024), nullable=True)
    slot_type = Column(
        String(32), nullable=False, server_default='feed', comment='feed / pre_roll / pause / detail / mine / player'
    )
    weight = Column(Integer, nullable=False, server_default='0')
    start_time = Column(DateTime, nullable=True, comment='生效开始')
    end_time = Column(DateTime, nullable=True, comment='生效结束')
    impression_count = Column(BigInteger, nullable=False, server_default='0', comment='曝光量')
    click_count = Column(BigInteger, nullable=False, server_default='0', comment='点击量')
    status = Column(CHAR(1), nullable=False, server_default='0', comment='0启用 1停用')
    create_time = Column(DateTime, nullable=True, default=datetime.now)


class DramaUserWatchHistory(Base):
    __tablename__ = 'drama_user_watch_history'
    __table_args__ = (
        UniqueConstraint('app_user_id', 'drama_id', name='uq_drama_watch_user_drama'),
        {'comment': '观看进度'},
    )

    history_id = Column(BigInteger, primary_key=True, autoincrement=True)
    app_user_id = Column(BigInteger, nullable=False)
    drama_id = Column(BigInteger, nullable=False)
    node_id = Column(BigInteger, nullable=True)
    progress_sec = Column(Integer, nullable=False, server_default='0')
    update_time = Column(DateTime, nullable=True, default=datetime.now, onupdate=datetime.now)


class DramaUserFavorite(Base):
    __tablename__ = 'drama_user_favorite'
    __table_args__ = (
        UniqueConstraint('app_user_id', 'drama_id', name='uq_drama_fav_user_drama'),
        {'comment': '收藏'},
    )

    fav_id = Column(BigInteger, primary_key=True, autoincrement=True)
    app_user_id = Column(BigInteger, nullable=False)
    drama_id = Column(BigInteger, nullable=False)
    create_time = Column(DateTime, nullable=True, default=datetime.now)


class DramaUserLike(Base):
    __tablename__ = 'drama_user_like'
    __table_args__ = (
        UniqueConstraint('app_user_id', 'target_type', 'target_id', name='uq_drama_like_target'),
        {'comment': '点赞'},
    )

    like_id = Column(BigInteger, primary_key=True, autoincrement=True)
    app_user_id = Column(BigInteger, nullable=False)
    target_type = Column(String(32), nullable=False, comment='drama / node')
    target_id = Column(BigInteger, nullable=False)
    create_time = Column(DateTime, nullable=True, default=datetime.now)


class DramaComment(Base):
    __tablename__ = 'drama_comment'
    __table_args__ = {'comment': '评论'}

    comment_id = Column(BigInteger, primary_key=True, autoincrement=True)
    app_user_id = Column(BigInteger, nullable=False)
    drama_id = Column(BigInteger, nullable=False)
    node_id = Column(BigInteger, nullable=True)
    content = Column(Text, nullable=False)
    status = Column(CHAR(1), nullable=False, server_default='0', comment='0正常 1隐藏')
    create_time = Column(DateTime, nullable=True, default=datetime.now)


class DramaUserChoiceLog(Base):
    __tablename__ = 'drama_user_choice_log'
    __table_args__ = {'comment': '用户分支选择记录'}

    log_id = Column(BigInteger, primary_key=True, autoincrement=True)
    app_user_id = Column(BigInteger, nullable=False)
    drama_id = Column(BigInteger, nullable=False)
    from_node_id = Column(BigInteger, nullable=True)
    choice_id = Column(BigInteger, nullable=False)
    to_node_id = Column(BigInteger, nullable=False)
    create_time = Column(DateTime, nullable=True, default=datetime.now)


class DramaUploadFile(Base):
    __tablename__ = 'drama_upload_file'
    __table_args__ = {'comment': '上传文件记录（TOS）'}

    file_id = Column(BigInteger, primary_key=True, autoincrement=True)
    object_key = Column(String(512), nullable=False, comment='对象键')
    bucket = Column(String(256), nullable=False)
    mime_type = Column(String(128), nullable=True)
    size_bytes = Column(BigInteger, nullable=True)
    drama_id = Column(BigInteger, nullable=True)
    node_id = Column(BigInteger, nullable=True)
    status = Column(String(32), nullable=False, server_default='pending', comment='pending / complete')
    create_by = Column(String(64), nullable=True, server_default="''", comment='后台用户')
    create_time = Column(DateTime, nullable=True, default=datetime.now)
