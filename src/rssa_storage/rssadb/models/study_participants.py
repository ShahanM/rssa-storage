"""SQLAlchemy models for study participants and related entities."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rssa_storage.rssadb.models.rssa_base_models import DBBaseParticipantResponseModel, RssaBase
from rssa_storage.shared import DateAuditMixin
from rssa_storage.shared.db_utils import PortableJSON

if TYPE_CHECKING:
    from rssa_storage.rssadb.models.participant_responses import (
        ParticipantAttentionCheckResponse,
        ParticipantFreeformResponse,
        ParticipantStudyInteractionResponse,
        ParticipantSurveyResponse,
    )
    from rssa_storage.rssadb.models.study_components import StudyCondition


class StudyParticipant(RssaBase, DateAuditMixin):
    """SQLAlchemy model for the 'study_participants' table."""

    __tablename__ = 'study_participants'

    study_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey('studies.id'))
    discarded: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False, server_default=sa.text('FALSE'))

    source_meta: Mapped[dict] = mapped_column(JSONB, nullable=True)
    study_condition_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey('study_conditions.id'))
    current_status: Mapped[str] = mapped_column(default='active')

    current_step_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey('study_steps.id'))
    current_page_id: Mapped[uuid.UUID | None] = mapped_column(sa.ForeignKey('study_step_pages.id'))

    participant_study_session: Mapped['ParticipantStudySession'] = relationship(
        'ParticipantStudySession', back_populates='study_participant', cascade='all, delete-orphan'
    )
    study_condition: Mapped['StudyCondition'] = relationship('StudyCondition', back_populates='study_participants')
    demographics: Mapped[list['Demographic']] = relationship(
        'Demographic', back_populates='study_participant', cascade='all, delete-orphan'
    )
    attention_check_responses: Mapped[list['ParticipantAttentionCheckResponse']] = relationship(
        'ParticipantAttentionCheckResponse', lazy='noload', viewonly=True
    )
    freeform_responses: Mapped[list['ParticipantFreeformResponse']] = relationship(
        'ParticipantFreeformResponse', lazy='noload', viewonly=True
    )
    activity_responses: Mapped[list['ParticipantStudyInteractionResponse']] = relationship(
        'ParticipantStudyInteractionResponse', lazy='noload', viewonly=True
    )
    survey_responses: Mapped[list['ParticipantSurveyResponse']] = relationship(lazy='noload', viewonly=True)

    @hybrid_property
    def prolific_pid(self) -> str | None:
        if self.source_meta and isinstance(self.source_meta, dict):
            return self.source_meta.get('PROLIFIC_PID')
        return None

    @prolific_pid.inplace.expression
    @classmethod
    def _prolific_pid_expression(cls):
        return cls.source_meta['PROLIFIC_PID'].astext


class Demographic(RssaBase, DateAuditMixin):
    """SQLAlchemy model for the 'demographics' table."""

    __tablename__ = 'participant_demographics'

    study_participant_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(), sa.ForeignKey('study_participants.id', ondelete='CASCADE')
    )
    age_range: Mapped[str | None] = mapped_column()
    gender: Mapped[str | None] = mapped_column()
    gender_other: Mapped[str | None] = mapped_column()
    race: Mapped[str | None] = mapped_column()
    race_other: Mapped[str | None] = mapped_column()
    education: Mapped[str | None] = mapped_column()
    country: Mapped[str | None] = mapped_column()
    state_region: Mapped[str | None] = mapped_column()
    urbanicity: Mapped[str | None] = mapped_column()

    raw_json: Mapped[dict] = mapped_column(JSONB)

    version: Mapped[int] = mapped_column(default=1, server_default=sa.text('1'))
    discarded: Mapped[bool] = mapped_column(default=False)

    study_participant: Mapped['StudyParticipant'] = relationship('StudyParticipant', back_populates='demographics')


class ParticipantStudySession(RssaBase, DateAuditMixin):
    """SQLAlchemy model for the 'participant_sessions' table.

    Attributes:
        id: Primary key.
        created_at: Timestamp of creation.
        study_participant_id: Foreign key to the study participant.
        resume_code: Resume code for the participant session.
        expires_at: Expiration timestamp for the session.
        is_active: Indicates if the session is active.
    """

    __tablename__ = 'participant_study_sessions'

    study_participant_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(), sa.ForeignKey('study_participants.id', ondelete='CASCADE')
    )
    resume_code: Mapped[str] = mapped_column()
    expires_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, server_default=sa.text('TRUE'))

    study_participant: Mapped['StudyParticipant'] = relationship(
        'StudyParticipant', back_populates='participant_study_session'
    )


class ParticipantRecommendationContext(DBBaseParticipantResponseModel, DateAuditMixin):
    """SQLAlchemy model for the 'participant_recommendation_context' table.

    Attributes:
        recommendations_json: JSON field storing recommendation context data.
    """

    __tablename__ = 'participant_recommendation_contexts'

    recommendations_json: Mapped[dict] = mapped_column(
        PortableJSON,
        nullable=False,
    )

    __table_args__ = (
        sa.UniqueConstraint(
            'study_id',
            'study_participant_id',
            'context_tag',
        ),
    )
