"""add content column to posts table

Revision ID: 20736c342e93
Revises: c411e95d759a
Create Date: 2025-09-26 01:18:29.747526

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20736c342e93'
down_revision: Union[str, Sequence[str], None] = 'c411e95d759a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
