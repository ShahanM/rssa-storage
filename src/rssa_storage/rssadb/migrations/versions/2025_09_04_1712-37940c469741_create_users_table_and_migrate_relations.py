"""Create users table and migrate relations

Revision ID: 37940c469741
Revises: 7823671e9051
Create Date: 2025-09-04 17:12:21.834170

"""

import uuid
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '37940c469741'
down_revision: str | None = '7823671e9051'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    users_table = op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('auth0_sub', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    )
    print("Created 'users' table.")

    op.create_table(
        'api_keys',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('key_hash', sa.String(), unique=True, nullable=False, index=True),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('study_id', UUID(as_uuid=True), sa.ForeignKey('study.id'), nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('last_used_at', sa.DateTime(), nullable=True),
    )
    print("Created 'api_keys' table.")

    conn = op.get_bind()
    unique_user_subs_query = """
        SELECT owner AS sub FROM study WHERE owner IS NOT NULL
        UNION
        SELECT created_by AS sub FROM study WHERE created_by IS NOT NULL;
    """

    results = conn.execute(sa.text(unique_user_subs_query)).fetchall()
    unique_subs = [row[0] for row in results]

    if unique_subs:
        users_to_insert = [{'id': uuid.uuid4(), 'auth0_sub': sub} for sub in unique_subs]
        op.bulk_insert(users_table, users_to_insert)
        print(f"Populated 'users' table with {len(users_to_insert)} unique users from 'study' table.")
    else:
        print("No existing users found in 'study' table to migrate.")

    op.add_column('study', sa.Column('owner_id', UUID(as_uuid=True), nullable=True))
    op.add_column('study', sa.Column('created_by_id', UUID(as_uuid=True), nullable=True))
    print("Added new foreign key columns to 'study' table.")

    op.execute("""
        UPDATE study
        SET owner_id = (SELECT id FROM users WHERE users.auth0_sub = study.owner)
        WHERE study.owner IS NOT NULL;
    """)
    op.execute("""
        UPDATE study
        SET created_by_id = (SELECT id FROM users WHERE users.auth0_sub = study.created_by)
        WHERE study.created_by IS NOT NULL;
    """)
    print("Backfilled new foreign key columns in 'study' table.")

    # op.alter_column('study', 'owner_id', nullable=False)
    op.create_foreign_key('fk_study_owner_id_users', 'study', 'users', ['owner_id'], ['id'])

    # op.alter_column('study', 'created_by_id', nullable=False)
    op.create_foreign_key('fk_study_created_by_id_users', 'study', 'users', ['created_by_id'], ['id'])
    print("Applied foreign key constraints to 'study' table.")

    op.drop_column('study', 'owner')
    op.drop_column('study', 'created_by')
    print("Cleaned up old columns from 'study' table.")


def downgrade() -> None:
    op.add_column('study', sa.Column('created_by', sa.VARCHAR(), nullable=True))
    op.add_column('study', sa.Column('owner', sa.VARCHAR(), nullable=True))
    print("Re-added old string columns to 'study' table.")

    op.execute("""
        UPDATE study
        SET owner = (SELECT auth0_sub FROM users WHERE users.id = study.owner_id);
    """)
    op.execute("""
        UPDATE study
        SET created_by = (SELECT auth0_sub FROM users WHERE users.id = study.created_by_id);
    """)
    print("Backfilled old string columns in 'study' table.")

    op.drop_constraint('fk_study_owner_id_users', 'study', type_='foreignkey')
    op.drop_constraint('fk_study_created_by_id_users', 'study', type_='foreignkey')
    print("Dropped foreign key constraints from 'study' table.")

    op.drop_column('study', 'owner_id')
    op.drop_column('study', 'created_by_id')
    print("Dropped new UUID foreign key columns from 'study' table.")

    op.drop_table('api_keys')
    print("Dropped 'api_keys' table.")
    op.drop_table('users')
    print("Dropped 'users' table.")
