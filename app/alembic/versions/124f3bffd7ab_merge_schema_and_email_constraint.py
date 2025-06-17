"""merge schema and email constraint

Revision ID: 124f3bffd7ab
Revises: 744418327ee9, ecde1ce89aa1
Create Date: 2025-06-17 10:07:43.186125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '124f3bffd7ab'
down_revision: Union[str, None] = ('744418327ee9', 'ecde1ce89aa1')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
