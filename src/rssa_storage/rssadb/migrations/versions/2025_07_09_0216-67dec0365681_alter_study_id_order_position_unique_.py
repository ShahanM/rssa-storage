"""alter (study_id, order_position) unique constraint to deferred on study_step

Revision ID: 67dec0365681
Revises: 2256a12c8836
Create Date: 2025-07-09 02:16:45.414653

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '67dec0365681'
down_revision: Union[str, None] = '2256a12c8836'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

INDEX_AND_CONSTRAINT_NAME = 'study_step_study_id_order_position_key'
TABLE_NAME = 'study_step'


def upgrade() -> None:
    op.drop_index(INDEX_AND_CONSTRAINT_NAME, table_name=TABLE_NAME)
    print('Index dropped successfully.')

    print(
        f"Adding new unique constraint '{INDEX_AND_CONSTRAINT_NAME}' to '{TABLE_NAME}' as DEFERRABLE INITIALLY DEFERRED"
    )
    op.create_unique_constraint(
        constraint_name=INDEX_AND_CONSTRAINT_NAME,
        table_name=TABLE_NAME,
        columns=['study_id', 'order_position'],
        deferrable=True,
        initially='deferred',
    )


def downgrade() -> None:
    op.drop_constraint(INDEX_AND_CONSTRAINT_NAME, table_name=TABLE_NAME, type_='unique')
    print('Constraint dropped successfully.')

    print(f"Recreating unique index '{INDEX_AND_CONSTRAINT_NAME}' on '{TABLE_NAME}'...")
    op.create_index(
        INDEX_AND_CONSTRAINT_NAME,
        TABLE_NAME,
        ['study_id', 'order_position'],
        unique=True,
    )
    print('Unique index recreated successfully.')
