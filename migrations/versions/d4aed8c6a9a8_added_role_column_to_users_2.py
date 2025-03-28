"""Added role column to users_2

Revision ID: d4aed8c6a9a8
Revises: 57a60974c3af
Create Date: 2025-03-27 23:23:09.288980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4aed8c6a9a8'
down_revision: Union[str, None] = '57a60974c3af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define the ENUM type
user_role_enum = sa.Enum("USER", "ADMIN", name="userrole")

def upgrade() -> None:
    """Upgrade schema."""
    # Create the ENUM type in the database before using it
    user_role_enum.create(op.get_bind(), checkfirst=True)

    # Add the 'role' column with the ENUM type
    op.add_column('users', sa.Column('role', user_role_enum, nullable=False, server_default="USER"))

def downgrade() -> None:
    """Downgrade schema."""
    # Remove the column first
    op.drop_column('users', 'role')

    # Drop the ENUM type from the database
    user_role_enum.drop(op.get_bind(), checkfirst=True)
