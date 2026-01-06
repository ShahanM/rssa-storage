"""SQLAlchemy models for survey constructs and related entities."""

import uuid

import sqlalchemy as sa
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rssa_storage.rssadb.models.rssa_base_models import RssaBase, RssaOrderedBase
from rssa_storage.shared import DateAuditMixin, EnabledMixin, SoftDeleteMixin


class SurveyItem(RssaOrderedBase, DateAuditMixin, SoftDeleteMixin, EnabledMixin):
    """SQLAlchemy model for the 'construct_items' table.

    Attributes:
        enabled: Indicates if the item is enabled.
        deleted_at: Timestamp of deletion.
        text: The text of the construct item.
        notes: Additional notes about the item.
        order_position: Position of the item in an ordered list.
        created_by_id: Foreign key to the user who created the item.
        construct_id: Foreign key to the associated survey construct.
    """

    __tablename__ = 'survey_items'

    text: Mapped[str] = mapped_column(sa.Text, nullable=False)  # Also used as its display_name
    notes: Mapped[str | None] = mapped_column(sa.Text)

    survey_construct_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('survey_constructs.id', ondelete='CASCADE'), nullable=False
    )

    survey_construct: Mapped['SurveyConstruct'] = relationship('SurveyConstruct', back_populates='survey_items')


class SurveyConstruct(RssaBase, DateAuditMixin, SoftDeleteMixin):
    """SQLAlchemy model for the 'survey_constructs' table.

    Attributes:
        deleted_at: Timestamp of deletion.
        name: Name of the survey construct.
        description: Description of the survey construct.
        created_by_id: Foreign key to the user who created the construct
    """

    __tablename__ = 'survey_constructs'

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    survey_items: Mapped[list[SurveyItem]] = relationship(
        'SurveyItem',
        back_populates='survey_construct',
        uselist=True,
        cascade='all, delete-orphan',
    )
    study_step_page_contents: Mapped[list['StudyStepPageContent']] = relationship(  # type: ignore # noqa: F821
        'StudyStepPageContent', back_populates='survey_construct', uselist=True
    )


class SurveyScale(RssaBase, DateAuditMixin, SoftDeleteMixin, EnabledMixin):
    """SQLAlchemy model for the 'construct_scales' table.

    Attributes:
        enabled: Indicates if the survey scale is enabled.
        deleted_at (Optional[datetime]): Timestamp of deletion.
        name: Name of the survey survey scale.
        description: Description of the survey scale.
        created_by_id: Foreign key to the user who created the scale.
    """

    __tablename__ = 'survey_scales'

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column()

    survey_scale_levels: Mapped[list['SurveyScaleLevel']] = relationship(
        'SurveyScaleLevel',
        back_populates='survey_scale',
        order_by='SurveyScaleLevel.order_position',
        collection_class=ordering_list('order_position'),
        uselist=True,
        cascade='all, delete-orphan',
    )
    study_step_page_contents: Mapped[list['StudyStepPageContent']] = relationship(  # type: ignore # noqa: F821
        'StudyStepPageContent', back_populates='survey_scale', uselist=True
    )


class SurveyScaleLevel(RssaOrderedBase, DateAuditMixin, SoftDeleteMixin, EnabledMixin):
    """SQLAlchemy model for the 'survey_scale_levels' table.

    Attributes:
        enabled: Indicates if the survey scale level is enabled.
        deleted_at: Timestamp of deletion.
        label: Label of the survey scale level.
        notes: Additional notes about the survey_scale level.
        value: Numeric value of the survey scale level.
        order_position: Position of the survey scale level in an ordered list.
        created_by_id: Foreign key to the user who created the survey scale level.
        scale_id: Foreign key to the associated survey scale.
    """

    __tablename__ = 'survey_scale_levels'

    label: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[str | None] = mapped_column()
    value: Mapped[int] = mapped_column(nullable=False)

    survey_scale_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('survey_scales.id', ondelete='CASCADE'), nullable=False
    )

    survey_scale: Mapped['SurveyScale'] = relationship('SurveyScale', back_populates='survey_scale_levels')
