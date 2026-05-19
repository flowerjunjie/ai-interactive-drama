"""drama mvp — 执行本地 drama_tables_mvp_mysql 脚本

Revision ID: 250515_drama
Revises:
Create Date: 2026-05-15

若表已由 SQLAlchemy create_all 创建，本迁移可能因表已存在失败，可标记为已应用:
  alembic stamp 250515_drama
"""

from collections.abc import Sequence
from pathlib import Path

import sqlalchemy as sa
from alembic import op

revision: str = '250515_drama'
down_revision: str | None = None  # 链首；后续见 250516_drama_align
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _sql_path() -> Path:
    return Path(__file__).resolve().parents[2] / 'sql' / 'drama_tables_mvp_mysql.sql'


def upgrade() -> None:
    sql_file = _sql_path()
    if not sql_file.exists():
        raise FileNotFoundError(f'缺少 {sql_file}')
    raw = sql_file.read_text(encoding='utf-8')
    for seg in raw.split(';'):
        stmt = seg.strip()
        if not stmt or stmt.startswith('--'):
            continue
        lines = [ln for ln in stmt.splitlines() if ln.strip() and not ln.strip().startswith('--')]
        if not lines:
            continue
        op.execute(sa.text('\n'.join(lines)))


def downgrade() -> None:
    for t in [
        'drama_upload_file',
        'drama_user_choice_log',
        'drama_comment',
        'drama_user_like',
        'drama_user_favorite',
        'drama_user_watch_history',
        'drama_ad',
        'drama_video_review',
        'drama_video_choice',
        'drama_video_node',
        'drama',
        'drama_app_user',
    ]:
        op.execute(sa.text(f'DROP TABLE IF EXISTS {t}'))
