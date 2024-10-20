"""Add new fields

Revision ID: 8f1f65be549e
Revises: c2a4de57d141
Create Date: 2024-10-19 12:57:08.034948

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8f1f65be549e"
down_revision: Union[str, None] = "c2a4de57d141"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("comments", sa.Column("is_deleted", sa.Boolean(), nullable=True))
    op.add_column("posts", sa.Column("is_deleted", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("posts", "is_deleted")
    op.drop_column("comments", "is_deleted")
    # ### end Alembic commands ###
