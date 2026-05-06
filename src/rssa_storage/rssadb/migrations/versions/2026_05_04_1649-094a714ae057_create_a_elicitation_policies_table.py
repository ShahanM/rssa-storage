"""create a elicitation_policies table

Revision ID: 094a714ae057
Revises: 45b299da3dcc
Create Date: 2026-05-04 16:49:27.377568

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = '094a714ae057'
down_revision: str | None = '45b299da3dcc'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'elicitation_policies',
        sa.Column('name', sa.String(), nullable=False),
        sa.Column(
            'elicitation_type',
            sa.Enum('ITEM_RATING', 'GENRE_SELECTION', 'TOPIC_PREFERENCE', name='elicitationtype'),
            nullable=False,
        ),
        sa.Column('min_threshold', sa.Integer(), nullable=False),
        sa.Column('domain', sa.String(), nullable=False),
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_elicitation_policies')),
    )
    op.add_column('studies', sa.Column('default_elicitation_policy_id', sa.UUID(), nullable=True))
    op.create_foreign_key(
        op.f('fk_studies_default_elicitation_policy_id'),
        'studies',
        'elicitation_policies',
        ['default_elicitation_policy_id'],
        ['id'],
    )
    op.add_column('study_conditions', sa.Column('override_policy_id', sa.UUID(), nullable=True))
    op.create_foreign_key(
        op.f('fk_study_conditions_override_policy_id'),
        'study_conditions',
        'elicitation_policies',
        ['override_policy_id'],
        ['id'],
    )


def downgrade() -> None:
    op.drop_constraint(op.f('fk_study_conditions_override_policy_id'), 'study_conditions', type_='foreignkey')
    op.drop_column('study_conditions', 'override_policy_id')
    op.drop_constraint(op.f('fk_studies_default_elicitation_policy_id'), 'studies', type_='foreignkey')
    op.drop_column('studies', 'default_elicitation_policy_id')
    op.drop_table('elicitation_policies')
