"""Seed data

Revision ID: 97956a213ec7
Revises: c2cf21c0e4e2
Create Date: 2025-10-08 17:30:50.880955

"""
import json
from pathlib import Path
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.config import settings


# revision identifiers, used by Alembic.
revision: str = '97956a213ec7'
down_revision: Union[str, Sequence[str], None] = 'c2cf21c0e4e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def insert_user():
    op.bulk_insert(
        sa.table('users',
            sa.column('id', sa.Integer),
            sa.column('name', sa.String),
            sa.column('email', sa.String),
            sa.column('api_key', sa.String)
        ),
        [{'id': 1, 'name': 'Will', 'email': 'foo@bar.baz', 'api_key': settings.API_KEY_MOCK}]
    )

def insert_questionnaires():
    seed_data = json.loads(Path('alembic/seed_data/questionnaires.json').read_text())
    op.bulk_insert(
        sa.table('questionnaires',
            sa.column('id', sa.Integer),
            sa.column('name', sa.String),
            sa.column('description', sa.String),
            sa.column('order', sa.Integer)
        ),
        seed_data
    )

def insert_items():
    seed_data = json.loads(Path('alembic/seed_data/items.json').read_text())
    op.bulk_insert(
        sa.table('items',
            sa.column('id', sa.Integer),
            sa.column('questionnaire_id', sa.Integer),
            sa.column('name', sa.String),
            sa.column('question', sa.JSON()),
            sa.column('content', sa.JSON()),
            sa.column('order', sa.Integer)
        ),
        seed_data
    )

def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    count = conn.execute(
        sa.text("SELECT COUNT(*) FROM users")
    ).scalar()

    if count != 0:
        print("Données déjà injectées.")
        return
    
    insert_user()
    insert_questionnaires()
    insert_items()


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM items")
    op.execute("DELETE FROM answers")
    op.execute("DELETE FROM sessions")
    op.execute("DELETE FROM questionnaires")
    op.execute("DELETE FROM users")
