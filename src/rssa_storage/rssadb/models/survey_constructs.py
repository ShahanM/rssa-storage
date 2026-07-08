"""SQLAlchemy models for survey constructs and related entities."""

import uuid
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rssa_storage.rssadb.models.rssa_base_models import RssaBase, RssaOrderedBase
from rssa_storage.shared import DateAuditMixin, EnabledMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from .study_components import StudyStepPageContent


class SurveyItem(RssaOrderedBase, DateAuditMixin, SoftDeleteMixin, EnabledMixin):
    """SQLAlchemy model for the 'construct_items' table."""

    __tablename__ = 'survey_items'

    text: Mapped[str] = mapped_column(sa.Text, nullable=False)  # Also used as its display_name
    notes: Mapped[str | None] = mapped_column(sa.Text)

    survey_construct_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('survey_constructs.id', ondelete='CASCADE'), nullable=False
    )

    is_negative: Mapped[bool] = mapped_column(
        sa.Boolean, nullable=False, default=False, server_default=sa.text('false')
    )

    survey_construct: Mapped['SurveyConstruct'] = relationship('SurveyConstruct', back_populates='survey_items')


class SurveyConstruct(RssaBase, DateAuditMixin, SoftDeleteMixin):
    """SQLAlchemy model for the 'survey_constructs' table."""

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
    """SQLAlchemy model for the 'construct_scales' table."""

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
    """SQLAlchemy model for the 'survey_scale_levels' table."""

    __tablename__ = 'survey_scale_levels'

    label: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[str | None] = mapped_column()
    value: Mapped[int] = mapped_column(nullable=False)

    survey_scale_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('survey_scales.id', ondelete='CASCADE'), nullable=False
    )

    survey_scale: Mapped['SurveyScale'] = relationship('SurveyScale', back_populates='survey_scale_levels')
