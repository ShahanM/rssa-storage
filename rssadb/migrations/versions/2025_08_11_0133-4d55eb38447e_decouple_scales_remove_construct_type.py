"""Decouple scales, remove construct_type

Revision ID: 4d55eb38447e
Revises: 91c00d8fbb1d
Create Date: 2025-08-11 01:33:12.184485

"""

import uuid
from datetime import datetime, timezone
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "4d55eb38447e"
down_revision: Union[str, None] = "91c00d8fbb1d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "page_content", sa.Column("scale_id", UUID(as_uuid=True), nullable=True)
    )
    op.create_foreign_key(
        "fk_page_content_scale_id",
        "page_content",
        "construct_scale",
        ["scale_id"],
        ["id"],
        ondelete="SET NULL",
    )
    print("Added 'scale_id' foreign key to 'page_content' table.")

    op.drop_constraint(
        "fk_survey_construct_construct_scale_id", "survey_construct", type_="foreignkey"
    )
    op.drop_column("survey_construct", "scale")
    print("Removed 'scale' foreign key from 'survey_construct'.")

    op.drop_constraint(
        "fk_survey_construct_construct_type_id", "survey_construct", type_="foreignkey"
    )
    op.drop_column("survey_construct", "type")
    print("Removed 'type' foreign key from 'survey_construct'.")

    op.drop_constraint(
        "fk_construct_item_construct_item_type_id", "construct_item", type_="foreignkey"
    )
    print("Removed 'construct_item_type' foreign key from 'construct_item'.")

    op.drop_column("construct_item", "item_type")
    print("Removed 'item_type' column from 'construct_item'.")

    op.drop_table("construct_item_type")
    print("Dropped 'construct_item_type' table.")

    op.drop_table("construct_type")
    print("Dropped 'construct_type' table.")

    op.drop_column("construct_scale", "levels")
    print("Removed 'levels' column from 'construct_scale'.")

    op.add_column(
        "construct_scale", sa.Column("description", sa.String(), nullable=True)
    )
    print("Added 'description' column to 'construct_scale'.")

    op.add_column(
        "construct_scale", sa.Column("created_by", sa.String(), nullable=True)
    )
    print("Added 'created_by' column to 'construct_scale'.")

    op.add_column(
        "construct_scale",
        sa.Column(
            "date_created",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    print("Added 'date_created' column to 'construct_scale'.")


def downgrade() -> None:
    op.drop_constraint("fk_page_content_scale_id", "page_content", type_="foreignkey")
    op.drop_column("page_content", "scale_id")
    print("Removed 'scale_id' from 'page_content' table.")

    op.drop_column("construct_scale", "description")
    print("Removed 'description' column from 'construct_scale'.")

    op.drop_column("construct_scale", "created_by")
    print("Removed 'created_by' column from 'construct_scale'.")

    op.drop_column("construct_scale", "date_created")
    print("Removed 'date_created' column from 'construct_scale'.")

    op.add_column(
        "construct_scale",
        sa.Column(
            "levels",
            sa.INTEGER(),
            autoincrement=False,
            nullable=False,
            server_default="0",
        ),
    )
    print("Re-added 'levels' column to 'construct_scale'.")

    op.create_table(
        "construct_type",
        sa.Column("id", UUID(as_uuid=True), nullable=False),
        sa.Column("type", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("enabled", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="construct_type_pkey"),
    )
    print("Re-created 'construct_type' table.")

    op.add_column(
        "survey_construct",
        sa.Column("type", UUID(as_uuid=True), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "fk_survey_construct_construct_type_id",
        "survey_construct",
        "construct_type",
        ["type"],
        ["id"],
    )
    print("Re-added 'type' foreign key to 'survey_construct'.")

    op.add_column(
        "survey_construct",
        sa.Column("scale", UUID(as_uuid=True), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "fk_survey_construct_construct_scale_id",
        "survey_construct",
        "construct_scale",
        ["scale"],
        ["id"],
    )
    print("Re-added 'scale' foreign key to 'survey_construct'.")

    op.create_table(
        "construct_item_type",
        sa.Column("id", UUID(as_uuid=True), nullable=False),
        sa.Column("type", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="construct_item_type_pkey"),
    )
    print("Re-created 'construct_item_type' table.")

    op.add_column(
        "construct_item",
        sa.Column("item_type", UUID(as_uuid=True), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "fk_construct_item_construct_item_type_id",
        "construct_item",
        "construct_item_type",
        ["item_type"],
        ["id"],
    )
    print("Re-added 'item_type' foreign key to 'construct_item'.")
