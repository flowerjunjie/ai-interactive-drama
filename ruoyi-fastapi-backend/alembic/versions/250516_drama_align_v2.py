"""drama MVP align v2 — idempotent column adds + data backfill

Revision ID: 250516_drama_align
Revises: 250515_drama
Create Date: 2026-05-15

与 sql/drama_tables_align_v2_mysql.sql 逻辑一致；手工执行 SQL 时请整文件运行（含 DELIMITER）。
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.mysql import CHAR


revision: str = '250516_drama_align'
down_revision: str | None = '250515_drama'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _has_column(bind: sa.Connection, table: str, column: str) -> bool:
    insp = sa.inspect(bind)
    cols = insp.get_columns(table)
    return any(c['name'] == column for c in cols)


def upgrade() -> None:
    bind = op.get_bind()

    if not _has_column(bind, 'drama', 'tags'):
        op.add_column(
            'drama',
            sa.Column('tags', sa.String(512), nullable=True, comment='标签 JSON 或逗号分隔'),
        )
    if not _has_column(bind, 'drama', 'heat'):
        op.add_column(
            'drama',
            sa.Column(
                'heat',
                sa.Integer(),
                nullable=False,
                server_default=sa.text('0'),
                comment='热度',
            ),
        )

    if not _has_column(bind, 'drama_video_node', 'episode_no'):
        op.add_column(
            'drama_video_node',
            sa.Column('episode_no', sa.Integer(), nullable=True, comment='集序号'),
        )
    if not _has_column(bind, 'drama_video_node', 'tos_key'):
        op.add_column(
            'drama_video_node',
            sa.Column('tos_key', sa.String(512), nullable=True, comment='TOS 对象键'),
        )
    if not _has_column(bind, 'drama_video_node', 'is_interactive'):
        op.add_column(
            'drama_video_node',
            sa.Column(
                'is_interactive',
                CHAR(1),
                nullable=False,
                server_default=sa.text("'0'"),
                comment='是否互动 0否1是',
            ),
        )
    if not _has_column(bind, 'drama_video_node', 'choice_trigger_sec'):
        op.add_column(
            'drama_video_node',
            sa.Column(
                'choice_trigger_sec',
                sa.Float(),
                nullable=True,
                comment='分支弹出时刻(秒)',
            ),
        )
    if not _has_column(bind, 'drama_video_node', 'review_status'):
        op.add_column(
            'drama_video_node',
            sa.Column(
                'review_status',
                sa.String(32),
                nullable=False,
                server_default=sa.text("'pending'"),
                comment='pending/approved/rejected',
            ),
        )
    if not _has_column(bind, 'drama_video_node', 'reject_reason'):
        op.add_column(
            'drama_video_node',
            sa.Column('reject_reason', sa.String(500), nullable=True, comment='审核拒绝原因'),
        )

    if _has_column(bind, 'drama_video_node', 'review_status'):
        op.execute(
            sa.text(
                "UPDATE drama_video_node SET review_status = 'approved' "
                "WHERE status = 'published' AND review_status = 'pending'"
            )
        )

    if not _has_column(bind, 'drama_video_choice', 'choice_code'):
        op.add_column(
            'drama_video_choice',
            sa.Column('choice_code', sa.String(8), nullable=True, comment='选项编码如 A/B/C'),
        )

    if not _has_column(bind, 'drama_ad', 'media_type'):
        op.add_column(
            'drama_ad',
            sa.Column(
                'media_type',
                sa.String(16),
                nullable=False,
                server_default=sa.text("'image'"),
                comment='image/video',
            ),
        )
    if not _has_column(bind, 'drama_ad', 'media_url'):
        op.add_column(
            'drama_ad',
            sa.Column('media_url', sa.String(1024), nullable=True, comment='主素材 URL'),
        )
    if not _has_column(bind, 'drama_ad', 'cover_url'):
        op.add_column(
            'drama_ad',
            sa.Column('cover_url', sa.String(1024), nullable=True, comment='视频封面'),
        )
    if not _has_column(bind, 'drama_ad', 'start_time'):
        op.add_column(
            'drama_ad',
            sa.Column('start_time', sa.DateTime(), nullable=True, comment='生效开始'),
        )
    if not _has_column(bind, 'drama_ad', 'end_time'):
        op.add_column(
            'drama_ad',
            sa.Column('end_time', sa.DateTime(), nullable=True, comment='生效结束'),
        )
    if not _has_column(bind, 'drama_ad', 'impression_count'):
        op.add_column(
            'drama_ad',
            sa.Column(
                'impression_count',
                sa.BigInteger(),
                nullable=False,
                server_default=sa.text('0'),
                comment='曝光',
            ),
        )
    if not _has_column(bind, 'drama_ad', 'click_count'):
        op.add_column(
            'drama_ad',
            sa.Column(
                'click_count',
                sa.BigInteger(),
                nullable=False,
                server_default=sa.text('0'),
                comment='点击',
            ),
        )

    if _has_column(bind, 'drama_ad', 'media_url') and _has_column(bind, 'drama_ad', 'image_url'):
        op.execute(
            sa.text(
                'UPDATE drama_ad SET media_url = image_url '
                'WHERE media_url IS NULL AND image_url IS NOT NULL'
            )
        )


def downgrade() -> None:
    # 非破坏性降级：仅移除新增列（生产慎用）
    pass
