"""create user model

Revision ID: d8bf3458eb7c
Revises: 545fe8f3bd43
Create Date: 2023-08-26 10:50:03.742528

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8bf3458eb7c'
down_revision: Union[str, None] = '545fe8f3bd43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
