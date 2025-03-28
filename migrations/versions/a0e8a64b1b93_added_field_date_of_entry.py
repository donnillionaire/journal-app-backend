"""added field date of entry

Revision ID: a0e8a64b1b93
Revises: cc2d9a46d603
Create Date: 2025-03-26 15:14:46.537277

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0e8a64b1b93'
down_revision: Union[str, None] = 'cc2d9a46d603'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('journals', sa.Column('date_of_entry', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('journals', 'date_of_entry')
    # ### end Alembic commands ###
