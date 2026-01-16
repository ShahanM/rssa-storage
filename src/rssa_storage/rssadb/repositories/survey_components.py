"""Repository for SurveyConstruct and related models."""

from sqlalchemy.orm import selectinload

from rssa_storage.rssadb.models.survey_constructs import SurveyConstruct, SurveyItem, SurveyScale, SurveyScaleLevel
from rssa_storage.shared import BaseOrderedRepository, BaseRepository


class SurveyConstructRepository(BaseRepository[SurveyConstruct]):
    """Repository for SurveyConstruct model."""

    SEARCHABLE_COLUMNS = ['name', 'description']
    LOAD_FULL_DETAILS = (selectinload(SurveyConstruct.survey_items),)


class SurveyScaleRepository(BaseRepository[SurveyScale]):
    """Repository for SurveyScale model."""

    LOAD_FULL_DETAILS = (selectinload(SurveyScale.survey_scale_levels),)
    SEARCHABLE_COLUMNS = ['name', 'description']


class SurveyItemRepository(BaseOrderedRepository[SurveyItem]):
    """Repository for SurveyItem model.

    Attributes:
        parent_id_column_name: Configures the BaseOrderedRepository to use 'survey_construct_id'
            as the parent ID column.
    """

    parent_id_column_name: str = 'survey_construct_id'


class SurveyScaleLevelRepository(BaseOrderedRepository[SurveyScaleLevel]):
    """Repository for SurveyScaleLevel model.

    Attributes:
        parent_id_column_name: Configures the BaseOrderedRepository to use 'survey_scale_id' as the parent ID column.
    """

    parent_id_column_name: str = 'survey_scale_id'
