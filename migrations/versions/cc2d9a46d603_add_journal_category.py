"""Add journal category

Revision ID: cc2d9a46d603
Revises: 3db0738a234a
Create Date: 2025-03-26 03:00:05.405572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc2d9a46d603'
down_revision: Union[str, None] = '3db0738a234a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Add a default value before setting NOT NULL
def upgrade():
    op.add_column('journals', sa.Column('journal_category', sa.String(), nullable=True))
    op.execute("UPDATE journals SET journal_category = 'Uncategorized' WHERE journal_category IS NULL")
    op.alter_column('journals', 'journal_category', nullable=False)

def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('journals', 'journal_category')
    # ### end Alembic commands ###
