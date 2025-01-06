"""Add indexes to Operator and Subscriber

Revision ID: bd40745c2f5d
Revises: 979c62672e79
Create Date: 2025-01-06 19:13:54.971461

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd40745c2f5d'
down_revision: Union[str, None] = '979c62672e79'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_index('ix_operator_region', 'operator', ['region'])
    op.create_index('ix_subscriber_email', 'subscriber', ['email'])


def upgrade():
    op.create_index('ix_operator_region', 'operator', ['region'])
    op.create_index('ix_subscriber_email', 'subscriber', ['email'])
