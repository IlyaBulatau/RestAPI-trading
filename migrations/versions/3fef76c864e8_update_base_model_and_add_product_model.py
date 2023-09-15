"""update base model and add product model

Revision ID: 3fef76c864e8
Revises: ef12f13f94b2
Create Date: 2023-09-15 16:49:15.146751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3fef76c864e8"
down_revision: Union[str, None] = "ef12f13f94b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
