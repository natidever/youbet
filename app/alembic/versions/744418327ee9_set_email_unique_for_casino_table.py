# """set email unique for Casino table

# Revision ID: 744418327ee9
# Revises: ecde1ce89aa1
# Create Date: 2025-06-17 09:49:17.394576

# """
# from typing import Sequence, Union

# from alembic import op
# import sqlalchemy as sa


# # revision identifiers, used by Alembic.
# revision: str = '744418327ee9'
# down_revision: Union[str, None] = 'ecde1ce89aa1'
# branch_labels: Union[str, Sequence[str], None] = None
# depends_on: Union[str, Sequence[str], None] = None


# def upgrade() -> None:
#     """Upgrade schema."""
#     # ### commands auto generated by Alembic - please adjust! ###
#     op.create_unique_constraint(None, 'casino', ['contact_email'])
#     # ### end Alembic commands ###


# def downgrade() -> None:
#     """Downgrade schema."""
#     # ### commands auto generated by Alembic - please adjust! ###
#     op.drop_constraint(None, 'casino', type_='unique')
#     # ### end Alembic commands ###

"""set email unique for Casino table

Revision ID: 744418327ee9
Revises: 03f00748c9a7
Create Date: 2025-06-17 09:49:17.394576

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = '744418327ee9'
down_revision: Union[str, None] = '03f00748c9a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    
    # Step 1: Clean default 'string' values and duplicates
    conn.execute(text("""
        -- First handle default 'string' values
        UPDATE casino 
        SET contact_email = NULL 
        WHERE contact_email = 'string';
        
        -- Then handle other duplicates
        WITH keep_rows AS (
            SELECT MIN(id) as id 
            FROM casino 
            WHERE contact_email IS NOT NULL
            GROUP BY contact_email
        )
        UPDATE casino
        SET contact_email = CONCAT('duplicate_', id, '@fixed.com')
        WHERE contact_email IS NOT NULL
        AND id NOT IN (SELECT id FROM keep_rows)
        AND contact_email IN (
            SELECT contact_email
            FROM casino
            GROUP BY contact_email
            HAVING COUNT(*) > 1
        );
    """))
    
    # Step 2: Add unique constraint
    op.create_unique_constraint(
        'uq_casino_contact_email',  # Named constraint
        'casino', 
        ['contact_email']
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        'uq_casino_contact_email', 
        'casino', 
        type_='unique'
    )