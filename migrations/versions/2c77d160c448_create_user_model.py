"""create user model

Revision ID: 2c77d160c448
Revises: d8bf3458eb7c
Create Date: 2023-08-26 12:01:32.044075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2c77d160c448"
down_revision: Union[str, None] = "d8bf3458eb7c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
