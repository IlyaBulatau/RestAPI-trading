"""create user model

Revision ID: 8001838bfebd
Revises: 2c77d160c448
Create Date: 2023-08-26 12:01:46.695495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8001838bfebd'
down_revision: Union[str, None] = '2c77d160c448'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
