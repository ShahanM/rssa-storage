import uuid
from collections.abc import Sequence

from sqlalchemy import Row, and_, func, select
from sqlalchemy.orm import selectinload

from rssa_storage.rssadb.models.participant_responses import Feedback
from rssa_storage.rssadb.models.study_components import (
    Study,
    StudyAuthorization,
    StudyCondition,
    StudyStep,
    StudyStepPage,
    StudyStepPageContent,
)
from rssa_storage.rssadb.models.study_participants import StudyParticipant
from rssa_storage.rssadb.models.survey_constructs import SurveyConstruct, SurveyScale
from rssa_storage.shared import BaseOrderedRepository, BaseRepository, OrderedRepoQueryOptions, RepoQueryOptions


class StudyRepository(BaseRepository[Study]):
    """Repository for Study model."""

    SEARCHABLE_COLUMNS = ['name', 'description']
    LOAD_FULL_DETAILS = (selectinload(Study.study_steps), selectinload(Study.study_conditions))

    async def _get_authorized_study_ids(self, user_id: uuid.UUID) -> list[uuid.UUID]:
        """Helper to fetch study IDs authorized for a user."""
        query = select(StudyAuthorization.study_id).where(StudyAuthorization.user_id == user_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_authorized_for_user(self, user_id: uuid.UUID, options: RepoQueryOptions = None) -> Sequence[Study]:
        """Get studies authorized for a specific user."""
        study_ids = await self._get_authorized_study_ids(user_id)

        if not study_ids:
            return []

        options = options or RepoQueryOptions()
        # Merge existing ID filters if any
        if options.ids:
            options.ids = list(set(options.ids) & set(study_ids))
            if not options.ids:
                return []
        else:
            options.ids = study_ids

        return await self.find_many(options)

    async def count_authorized_for_user(self, user_id: uuid.UUID, search: str | None = None) -> int:
        """Count studies authorized for a specific user."""
        study_ids = await self._get_authorized_study_ids(user_id)

        if not study_ids:
            return 0

        return await self.count(filter_str=search, filter_cols=self.SEARCHABLE_COLUMNS, filters={'id': study_ids})


class StudyAuthorizationRepository(BaseRepository[StudyAuthorization]):
    """Repository for StudyAuthorization model."""

    pass


class StudyStepRepository(BaseOrderedRepository[StudyStep]):
    """Repository for StudyStep model.

    Attributes:
        parent_id_column_name: Configured the BaseOrderedRepository to use 'study_id' as the parent ID column.
    """

    parent_id_column_name: str = 'study_id'

    async def validate_path_uniqueness(
        self, study_id: uuid.UUID, path: str, exclude_step_id: uuid.UUID | None = None
    ) -> bool:
        """Validate that a StudyStep path is unique within a study, optionally excluding a specific step ID.

        Args:
            study_id: The UUID of the study.
            path: The path to validate.
            exclude_step_id: An optional UUID of a step to exclude from the check.

        Returns:
            True if the path is unique within the study, False otherwise.
        """
        query = select(StudyStep).where(and_(StudyStep.study_id == study_id, StudyStep.path == path))
        if exclude_step_id:
            query = query.where(StudyStep.id != exclude_step_id)

        existing_step = await self.db.execute(query)

        if existing_step.first():
            return False

        return True


class StudyStepPageRepository(BaseOrderedRepository[StudyStepPage]):
    """Repository for StudyStepPage model.

    Attributes:
        parent_id_column_name: Configured the BaseOrderedRepository to use 'study_id' as the parent ID column.
    """

    parent_id_column_name: str = 'study_step_id'

    SEARCHABLE_COLUMNS = ['name', 'description']
    LOAD_FULL_DETAILS = (
        selectinload(StudyStepPage.study_step_page_contents)
        .selectinload(StudyStepPageContent.survey_construct)
        .selectinload(SurveyConstruct.survey_items),
        selectinload(StudyStepPage.study_step_page_contents).selectinload(StudyStepPageContent.survey_construct),
        selectinload(StudyStepPage.study_step_page_contents)
        .selectinload(StudyStepPageContent.survey_scale)
        .selectinload(SurveyScale.survey_scale_levels),
    )


class StudyConditionRepository(BaseRepository[StudyCondition]):
    """Repository for StudyCondition model.

    Attributes:
        db: The database session.
        model: The StudyCondition model class.
    """

    async def get_participant_count_by_condition(self, study_id: uuid.UUID) -> list[Row[tuple[uuid.UUID, str, int]]]:
        """Get participant counts grouped by study conditions for a specific study.

        Args:
            study_id: The UUID of the study.

        Returns:
            A list of rows containing condition ID, condition name, and participant count.
        """
        condition_counts_query = (
            select(
                StudyCondition.id.label('study_condition_id'),
                StudyCondition.name.label('study_condition_name'),
                func.count(StudyParticipant.id).label('participant_count'),
            )
            .join(StudyParticipant, StudyParticipant.study_condition_id == StudyCondition.id, isouter=True)
            .where(StudyCondition.study_id == study_id)
            .group_by(StudyCondition.id, StudyCondition.name)
            .order_by(StudyCondition.name)
        )

        condition_counts_query = self._apply_soft_delete(condition_counts_query)

        condition_counts_result = await self.db.execute(condition_counts_query)
        condition_counts_rows = condition_counts_result.all()

        return list(condition_counts_rows)


class StudyStepPageContentRepository(BaseOrderedRepository[StudyStepPageContent]):
    """Repository for PageContent model.

    Attributes:
        parent_id_column_name: Configured the BaseOrderedRepository to use 'study_step_page_id' as the parent ID column.
    """

    parent_id_column_name: str = 'study_step_page_id'

    DETAILED_LOAD_OPTIONS = (
        selectinload(StudyStepPageContent.survey_construct).selectinload(SurveyConstruct.survey_items),
        selectinload(StudyStepPageContent.survey_scale).selectinload(SurveyScale.survey_scale_levels),
    )

    async def get_all_ordered_instances(
        self,
        parent_id: uuid.UUID,
        limit: int | None = None,
        include_deleted: bool = False,
    ) -> Sequence[StudyStepPageContent]:
        """Get all ordered instances for a given parent ID with detailed load options.

        Args:
            parent_id: The parent ID.
            limit: Optional limit on the number of instances to retrieve.
            include_deleted: Whether to include soft-deleted instances.

        Returns:
            A list of ordered instances with relationships loaded.
        """
        options = OrderedRepoQueryOptions(
            filters={self.parent_id_column_name: parent_id},
            sort_by='order_position',
            sort_desc=False,
            limit=limit,
            include_deleted=include_deleted,
            load_options=self.DETAILED_LOAD_OPTIONS,
        )
        return await self.find_many(options)


class FeedbackRepository(BaseRepository[Feedback]):
    """Repository for managing Feedback entities in the database.

    Inherits from BaseRepository to provide CRUD operations for Feedback model.
    """

    pass
