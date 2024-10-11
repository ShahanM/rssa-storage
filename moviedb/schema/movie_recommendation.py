from ..dbconfig import Base
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa
import uuid
from datetime import datetime, timezone


class MovieRecommendationText(Base):
	__tablename__ = 'movie_recommendation_text'

	id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

	movie_id = sa.Column(UUID(as_uuid=True), nullable=False, unique=True)
	formal = sa.Column(sa.String, nullable=False)
	informal = sa.Column(sa.String, nullable=False)

	created_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))
	updated_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))

	sa.ForeignKeyConstraint(['movie_id'], ['movies.id'])

	def __init__(self, movie_id: UUID, formal: str, informal: str):
		self.movie_id = movie_id
		self.formal = formal
		self.informal = informal