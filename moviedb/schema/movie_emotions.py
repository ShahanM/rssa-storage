from dbconfig import Base
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa
import uuid


class MovieEmotions(Base):
	__tablename__ = 'movie_emotions'

	id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

	movie_id = sa.Column(UUID(as_uuid=True), nullable=False, unique=True)
	movielens_id = sa.Column(sa.String, nullable=False)
	anger = sa.Column(sa.Numeric, nullable=False)
	anticipation = sa.Column(sa.Numeric, nullable=False)
	disgust = sa.Column(sa.Numeric, nullable=False)
	fear = sa.Column(sa.Numeric, nullable=False)
	joy = sa.Column(sa.Numeric, nullable=False)
	surprise = sa.Column(sa.Numeric, nullable=False)
	sadness = sa.Column(sa.Numeric, nullable=False)
	trust = sa.Column(sa.Numeric, nullable=False)
	iers_count = sa.Column(sa.Integer, nullable=False)
	iers_rank = sa.Column(sa.Integer, nullable=False)

	sa.ForeignKeyConstraint(['movie_id'], ['movies.id'])

	def __init__(self, movie_id: UUID, movielens_id:str, anger: float, anticipation: float,
		disgust: float, fear: float, joy: float, surprise: float,
		sadness: float, trust: float, iers_count: int, iers_rank: int):
		self.movie_id = movie_id
		self.movielens_id = movielens_id
		self.anger = anger
		self.anticipation = anticipation
		self.disgust = disgust
		self.fear = fear
		self.joy = joy
		self.surprise = surprise
		self.sadness = sadness
		self.trust = trust
		self.iers_count = iers_count
		self.iers_rank = iers_rank