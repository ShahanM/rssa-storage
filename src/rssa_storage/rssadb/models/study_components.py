"""SQLAlchemy models for study components in the RSSA API."""

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


class Study(RssaBase, DateAuditMixin, SoftDeleteMixin):
    """SQLAlchemy model for the 'studies' table.

    Attributes:
        enabled: Indicates if the study is active.
        name: Name of the study.
        description: Description of the study.
        created_by_id: Foreign key to the user who created the study.
        owner_id: Foreign key to the owner of the study.
    """

    __tablename__ = 'studies'

    enabled: Mapped[bool] = mapped_column(default=True)

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column()

    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        sa.UUID(),
        sa.ForeignKey('users.id', ondelete='SET NULL'),
    )
    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        sa.UUID(),
        sa.ForeignKey('users.id', ondelete='SET NULL'),
    )

    created_by: Mapped['User'] = relationship('User', back_populates='studies_created', foreign_keys=[created_by_id])
    owner: Mapped['User'] = relationship('User', back_populates='studies_owned', foreign_keys=[owner_id])

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
    """SQLAlchemy model for the 'study_conditions' table.

    Attributes:
        enabled: Indicates if the condition is active.
        name: Name of the study condition.
        description: Description of the study condition.
        recommendation_count: Number of recommendations associated with the condition.
        study_id: Foreign key to the associated study.
        created_by_id: Foreign key to the user who created the condition.
    """

    __tablename__ = 'study_conditions'

    # Metadata
    enabled: Mapped[bool] = mapped_column(default=True)

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column()
    recommender_key: Mapped[str | None] = mapped_column()
    recommendation_count: Mapped[int] = mapped_column(default=10)

    short_code: Mapped[str] = mapped_column(
        sa.String(48),
        nullable=False,
        default=generate_ref_code,
    )

    study_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey('studies.id', ondelete='CASCADE'), nullable=False)

    study: Mapped['Study'] = relationship('Study', back_populates='study_conditions')
    study_participants: Mapped[list['StudyParticipant']] = relationship(
        'StudyParticipant', back_populates='study_condition', uselist=True, cascade='all, delete-orphan'
    )

    __table_args__ = (sa.UniqueConstraint('study_id', 'short_code', deferrable=True, initially='DEFERRED'),)


class StudyStep(RssaOrderedBase, DateAuditMixin, SoftDeleteMixin):
    """SQLAlchemy model for the 'study_steps' table.

    Attributes:
        enabled: Indicates if the study step is active.
        deleted_at: Timestamp of deletion for soft deletes.
        step_type: Type of the study step.
        name: Name of the study step.
        description: Description of the study step.
        title: Title of the study step.
        instructions: Instructions for the study step.
        path: Path associated with the study step.
        survey_api_root: API root for surveys in the study step.
        study_id: Foreign key to the associated study.
        created_by_id: Foreign key to the user who created the step.
    """

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
    """SQLAlchemy model for the 'page_contents' table.

    Attributes:
        enabled: Indicates if the page content is active.
        created_by_id: Foreign key to the user who created the content.
        preamble: Preamble text for the page content.
        page_id: Foreign key to the associated page.
        construct_id: Foreign key to the associated survey construct.
        scale_id: Foreign key to the associated construct scale.
    """

    __tablename__ = 'study_step_page_contents'

    enabled: Mapped[bool] = mapped_column(default=True)

    preamble: Mapped[str | None] = mapped_column(sa.Text)

    study_step_page_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(), sa.ForeignKey('study_step_pages.id', ondelete='CASCADE'), primary_key=True
    )
    survey_construct_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID(), sa.ForeignKey('survey_constructs.id', ondelete='CASCADE'), primary_key=True
    )
    survey_scale_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('survey_scales.id', ondelete='CASCADE'), primary_key=True
    )

    study_step_page: Mapped['StudyStepPage'] = relationship('StudyStepPage', back_populates='study_step_page_contents')
    survey_construct: Mapped['SurveyConstruct'] = relationship(
        'SurveyConstruct', back_populates='study_step_page_contents'
    )
    survey_scale: Mapped['SurveyScale'] = relationship('SurveyScale', back_populates='study_step_page_contents')

    @property
    def name(self) -> str:
        """Get the display name for the content."""
        if self.survey_construct:
            return self.survey_construct.name
        return 'Unknown Content'


class StudyStepPage(RssaOrderedBase, DateAuditMixin, SoftDeleteMixin):
    """SQLAlchemy model for the 'study_step_pages' table.

    Attributes:
        enabled: Indicates if the page is active.
        page_type: Type of the page.
        name: Name of the page.
        description: Description of the page.
        title: Title of the page.
        instructions: Instructions for the page.
        created_by_id: Foreign key to the user who created the page.
        study_id: Foreign key to the associated study.
        step_id: Foreign key to the associated study step.
    """

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
    """SQLAlchemy model for the 'api_keys' table.

    Attributes:
        key_hash: Hashed value of the API key.
        description: Description of the API key.
        study_id: Foreign key to the associated study.
        user_id: Foreign key to the associated user.
        is_active: Indicates if the API key is active.
        created_at: Timestamp of creation.
        last_used_at: Timestamp of last usage.
    """

    __tablename__ = 'api_keys'

    key_hash: Mapped[str] = mapped_column(index=True, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)

    study_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey('studies.id', ondelete='CASCADE'), nullable=False)
    user_id: Mapped[uuid.UUID | None] = mapped_column(sa.ForeignKey('users.id', ondelete='CASCADE'))

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    last_used_at: Mapped[datetime | None] = mapped_column(sa.DateTime(timezone=True))

    study: Mapped['Study'] = relationship('Study', back_populates='api_keys')
    user: Mapped['User'] = relationship('User', back_populates='api_keys')


class User(RssaBase, DateAuditMixin):
    """SQLAlchemy model for the 'users' table.

    Attributes:
        auth0_sub: Unique Auth0 subject identifier.
        created_at: Timestamp of creation.
        studies_owned: List of studies owned by the user.
        studies_created: List of studies created by the user.
        api_keys: List of API keys associated with the user.
    """

    __tablename__ = 'users'

    auth0_sub: Mapped[str] = mapped_column(unique=True, index=True)
    studies_owned: Mapped[list['Study']] = relationship(
        'Study',
        back_populates='owner',
        foreign_keys='Study.owner_id',
    )
    studies_created: Mapped[list['Study']] = relationship(
        'Study', back_populates='created_by', foreign_keys='Study.created_by_id'
    )

    api_keys: Mapped[list['ApiKey']] = relationship('ApiKey', back_populates='user')
