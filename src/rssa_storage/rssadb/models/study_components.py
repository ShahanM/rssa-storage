"""SQLAlchemy models for study components in the RSSA API."""

import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rssa_storage.rssadb.models.rssa_base_models import RssaBase, RssaOrderedBase
from rssa_storage.rssadb.models.survey_constructs import SurveyConstruct, SurveyScale
from rssa_storage.shared import DateAuditMixin, SoftDeleteMixin
from rssa_storage.shared.generators import generate_ref_code

if TYPE_CHECKING:
    from rssa_storage.rssadb.models.study_participants import StudyParticipant


class ElicitationType(enum.Enum):
    ITEM_RATING = 'item_rating'
    GENRE_SELECTION = 'genre_selection'
    TOPIC_PREFERENCE = 'topic_preference'


class ElicitationPolicy(RssaBase, DateAuditMixin, SoftDeleteMixin):
    """SQLAlchemy model for the 'elicitation_policies' table."""

    __tablename__ = 'elicitation_policies'

    name: Mapped[str] = mapped_column()
    elicitation_type: Mapped[ElicitationType] = mapped_column()
    min_threshold: Mapped[int] = mapped_column()
    domain: Mapped[str] = mapped_column()

    studies: Mapped[list['Study']] = relationship(back_populates='default_elicitation_policy')


class Study(RssaBase, DateAuditMixin, SoftDeleteMixin):
    """SQLAlchemy model for the 'studies' table."""

    __tablename__ = 'studies'

    enabled: Mapped[bool] = mapped_column(default=True)

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column()

    completion_code: Mapped[str | None] = mapped_column()
    redirect_url: Mapped[str | None] = mapped_column()
    dataset_subset: Mapped[str | None] = mapped_column()

    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        sa.UUID(),
        sa.ForeignKey('users.id', ondelete='SET NULL'),
    )
    created_by: Mapped['User'] = relationship('User', back_populates='studies_created', foreign_keys=[created_by_id])

    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        sa.UUID(),
        sa.ForeignKey('users.id', ondelete='SET NULL'),
    )
    owner: Mapped['User'] = relationship('User', back_populates='studies_owned', foreign_keys=[owner_id])

    default_elicitation_policy_id: Mapped[uuid.UUID | None] = mapped_column(
        sa.UUID(), sa.ForeignKey('elicitation_policies.id')
    )
    default_elicitation_policy: Mapped['ElicitationPolicy'] = relationship(back_populates='studies')

    authorizations: Mapped[list['StudyAuthorization']] = relationship(
        'StudyAuthorization', back_populates='study', cascade='all, delete-orphan'
    )
    study_steps: Mapped[list['StudyStep']] = relationship(
        'StudyStep',
        back_populates='study',
        uselist=True,
        cascade='all, delete-orphan',
        order_by='StudyStep.order_position',
    )
    study_conditions: Mapped[list['StudyCondition']] = relationship(
        'StudyCondition', back_populates='study', uselist=True, cascade='all, delete-orphan'
    )
    api_keys: Mapped[list['ApiKey']] = relationship('ApiKey', back_populates='study', cascade='all, delete-orphan')


class StudyCondition(RssaBase, DateAuditMixin, SoftDeleteMixin):
    """SQLAlchemy model for the 'study_conditions' table."""

    __tablename__ = 'study_conditions'

    enabled: Mapped[bool] = mapped_column(default=True)

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column()
    recommender_key: Mapped[str | None] = mapped_column()
    recommendation_count: Mapped[int] = mapped_column(default=10)

    short_code: Mapped[str] = mapped_column(sa.String(48), nullable=False, default=generate_ref_code)
    view_link_key: Mapped[str | None] = mapped_column(sa.String(48), nullable=True)
    authorized_test_code: Mapped[str] = mapped_column(sa.String(16), nullable=True)

    study_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey('studies.id', ondelete='CASCADE'), nullable=False)
    study: Mapped['Study'] = relationship('Study', back_populates='study_conditions')

    override_policy_id: Mapped[uuid.UUID | None] = mapped_column(sa.UUID(), sa.ForeignKey('elicitation_policies.id'))
    override_policy: Mapped[ElicitationPolicy | None] = relationship()

    study_participants: Mapped[list['StudyParticipant']] = relationship(
        'StudyParticipant', back_populates='study_condition', uselist=True, cascade='all, delete-orphan'
    )

    __table_args__ = (sa.UniqueConstraint('study_id', 'short_code', deferrable=True, initially='DEFERRED'),)

    @property
    def active_policy(self) -> ElicitationPolicy | None:
        """Helper to safely resolve the effective policy for this condition."""
        return self.override_policy or self.study.default_elicitation_policy


class StudyStep(RssaOrderedBase, DateAuditMixin, SoftDeleteMixin):
    """SQLAlchemy model for the 'study_steps' table."""

    __tablename__ = 'study_steps'

    enabled: Mapped[bool] = mapped_column(default=True)

    step_type: Mapped[str | None] = mapped_column(nullable=True)

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column()

    title: Mapped[str | None] = mapped_column(sa.Text)
    instructions: Mapped[str | None] = mapped_column(sa.Text)

    path: Mapped[str] = mapped_column()
    survey_api_root: Mapped[str | None] = mapped_column()

    study_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(), sa.ForeignKey('studies.id', ondelete='CASCADE'), nullable=False
    )

    study: Mapped['Study'] = relationship('Study', back_populates='study_steps')
    study_step_pages: Mapped[list['StudyStepPage']] = relationship(
        'StudyStepPage', back_populates='study_step', uselist=True, cascade='all, delete-orphan'
    )

    __table_args__ = (
        sa.UniqueConstraint('study_id', 'order_position'),
        sa.UniqueConstraint(
            'study_id',
            'path',
            deferrable=True,
            initially='deferred',
        ),
    )


class StudyStepPageContent(RssaOrderedBase, DateAuditMixin, SoftDeleteMixin):
    """SQLAlchemy model for the 'page_contents' table."""

    __tablename__ = 'study_step_page_contents'

    enabled: Mapped[bool] = mapped_column(default=True)

    preamble: Mapped[str | None] = mapped_column(sa.Text)

    study_step_page_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(), sa.ForeignKey('study_step_pages.id', ondelete='CASCADE')
    )
    survey_construct_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(), sa.ForeignKey('survey_constructs.id', ondelete='CASCADE')
    )
    survey_scale_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey('survey_scales.id', ondelete='CASCADE'))

    study_step_page: Mapped['StudyStepPage'] = relationship('StudyStepPage', back_populates='study_step_page_contents')
    survey_construct: Mapped['SurveyConstruct'] = relationship(
        'SurveyConstruct', back_populates='study_step_page_contents'
    )
    survey_scale: Mapped['SurveyScale'] = relationship('SurveyScale', back_populates='study_step_page_contents')

    study_attention_check: Mapped['StudyAttentionCheck | None'] = relationship(
        'StudyAttentionCheck',
        back_populates='study_step_page_content',
    )

    @property
    def name(self) -> str:
        """Get the display name for the content."""
        if self.survey_construct:
            return self.survey_construct.name
        return 'Unknown Content'


class StudyAttentionCheck(RssaBase, DateAuditMixin):
    """Defines an attention check injected into a specific study page."""

    __tablename__ = 'study_attention_checks'

    text: Mapped[str] = mapped_column()
    assigned_position: Mapped[int] = mapped_column()

    study_step_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey('study_steps.id', ondelete='CASCADE'))
    study_step_page_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey('study_step_pages.id', ondelete='CASCADE'))
    study_step_page_content_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('study_step_page_contents.id', ondelete='CASCADE')
    )

    survey_scale_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey('survey_scales.id'))
    expected_survey_scale_level_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey('survey_scale_levels.id'))

    study_step_page_content: Mapped['StudyStepPageContent'] = relationship(
        'StudyStepPageContent', back_populates='study_attention_check'
    )


class StudyStepPage(RssaOrderedBase, DateAuditMixin, SoftDeleteMixin):
    """SQLAlchemy model for the 'study_step_pages' table."""

    __tablename__ = 'study_step_pages'

    enabled: Mapped[bool] = mapped_column(default=True)

    page_type: Mapped[str | None] = mapped_column('page_type', nullable=True)

    name: Mapped[str] = mapped_column()
    description: Mapped[str | None] = mapped_column()

    title: Mapped[str | None] = mapped_column(sa.Text)
    instructions: Mapped[str | None] = mapped_column(sa.Text)

    study_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(), sa.ForeignKey('studies.id', ondelete='CASCADE'), nullable=False
    )
    study_step_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(), sa.ForeignKey('study_steps.id', ondelete='CASCADE'), nullable=False
    )

    study_step: Mapped['StudyStep'] = relationship('StudyStep', back_populates='study_step_pages')
    study_step_page_contents: Mapped[list[StudyStepPageContent]] = relationship(
        'StudyStepPageContent', back_populates='study_step_page', uselist=True, cascade='all, delete-orphan'
    )

    __table_args__ = (sa.UniqueConstraint('study_step_id', 'order_position'),)


class ApiKey(RssaBase, DateAuditMixin):
    """SQLAlchemy model for the 'api_keys' table."""

    __tablename__ = 'api_keys'

    key_hash: Mapped[str] = mapped_column(index=True, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)

    study_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey('studies.id', ondelete='CASCADE'), nullable=False)
    user_id: Mapped[uuid.UUID | None] = mapped_column(sa.ForeignKey('users.id', ondelete='CASCADE'))

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    last_used_at: Mapped[datetime | None] = mapped_column(sa.DateTime(timezone=True))

    study: Mapped['Study'] = relationship('Study', back_populates='api_keys')
    user: Mapped['User'] = relationship('User', back_populates='api_keys')


class StudyAuthorization(RssaBase, DateAuditMixin):
    """SQLAlchemy model for the 'study_authorizations' table."""

    __tablename__ = 'study_authorizations'

    study_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey('studies.id', ondelete='CASCADE'), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    role: Mapped[str] = mapped_column(nullable=False)

    study: Mapped['Study'] = relationship('Study', back_populates='authorizations')
    user: Mapped['User'] = relationship('User', back_populates='study_authorizations')

    # Ensure a user is only authorized once for a given study
    __table_args__ = (
        sa.UniqueConstraint('study_id', 'user_id'),
        sa.Index(None, 'user_id'),
    )


class User(RssaBase, DateAuditMixin):
    """SQLAlchemy model for the 'users' table."""

    __tablename__ = 'users'

    auth0_sub: Mapped[str] = mapped_column(unique=True, index=True)

    email: Mapped[str | None] = mapped_column(nullable=True)
    desc: Mapped[str | None] = mapped_column(nullable=True)
    picture: Mapped[str | None] = mapped_column(nullable=True)
    studies_owned: Mapped[list['Study']] = relationship(
        'Study',
        back_populates='owner',
        foreign_keys='Study.owner_id',
    )
    studies_created: Mapped[list['Study']] = relationship(
        'Study', back_populates='created_by', foreign_keys='Study.created_by_id'
    )

    api_keys: Mapped[list['ApiKey']] = relationship('ApiKey', back_populates='user')
    study_authorizations: Mapped[list['StudyAuthorization']] = relationship(
        'StudyAuthorization', back_populates='user', cascade='all, delete-orphan'
    )
