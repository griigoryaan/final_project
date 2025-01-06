"""Add new columns to Operator and Subscriber

Revision ID: 979c62672e79
Revises: 
Create Date: 2025-01-06 19:02:10.874011

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '979c62672e79'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем колонку `region` в таблицу `Operator`
    op.add_column('operator', sa.Column('region', sa.String(length=100), nullable=True))
    
    # Добавляем колонку `email` в таблицу `Subscriber`
    op.add_column('subscriber', sa.Column('email', sa.String(length=255), nullable=True, unique=True))


def downgrade() -> None:
    # Удаляем колонку `region` из таблицы `Operator`
    op.drop_column('operator', 'region')
    
    # Удаляем колонку `email` из таблицы `Subscriber`
    op.drop_column('subscriber', 'email')
