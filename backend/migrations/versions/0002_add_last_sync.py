"""add last_sync to energy record

Revision ID: 0002
Revises: 0001
Create Date: 2026-03-27 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0002'
down_revision: Union[str, None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('monthly_energy', sa.Column('last_sync', sa.DateTime(), nullable=True))

def downgrade() -> None:
    op.drop_column('monthly_energy', 'last_sync')
