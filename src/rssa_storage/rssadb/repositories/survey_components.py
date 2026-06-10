"""Repository for SurveyConstruct and related models."""

from rssa_storage.rssadb.models.survey_constructs import SurveyConstruct, SurveyItem, SurveyScale, SurveyScaleLevel
from rssa_storage.shared import BaseOrderedRepository, BaseRepository


class SurveyConstructRepository(BaseRepository[SurveyConstruct]):
    """Repository for SurveyConstruct model."""

    SEARCHABLE_COLUMNS = ['name', 'description']


class SurveyScaleRepository(BaseRepository[SurveyScale]):
    """Repository for SurveyScale model."""

    SEARCHABLE_COLUMNS = ['name', 'description']


class SurveyItemRepository(BaseOrderedRepository[SurveyItem]):
    """Repository for SurveyItem model."""

    parent_id_column_name: str = 'survey_construct_id'


class SurveyScaleLevelRepository(BaseOrderedRepository[SurveyScaleLevel]):
    """Repository for SurveyScaleLevel model."""

    parent_id_column_name: str = 'survey_scale_id'
