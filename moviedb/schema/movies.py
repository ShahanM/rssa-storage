from ..dbconfig import Base
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa
import uuid

class Movie(Base):
	__tablename__ = 'movies'

	id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

	movielens_id = sa.Column(sa.String, nullable=False, unique=True)
	tmdb_id = sa.Column(sa.String, nullable=True)
	imdb_id = sa.Column(sa.String, nullable=False)
	title = sa.Column(sa.String, nullable=False)
	year = sa.Column(sa.Integer, nullable=False)
	runtime = sa.Column(sa.Integer, nullable=False)
	genre = sa.Column(sa.String, nullable=False)
	ave_rating = sa.Column(sa.Numeric, nullable=False)
	director = sa.Column(sa.Text, nullable=False)
	writer = sa.Column(sa.Text, nullable=False)
	description = sa.Column(sa.Text, nullable=False)
	cast = sa.Column(sa.Text, nullable=False)
	poster = sa.Column(sa.String, nullable=False)
	count = sa.Column(sa.Integer, nullable=False)
	rank = sa.Column(sa.Integer, nullable=False)
	poster_identifier = sa.Column(sa.String, nullable=False)

	def __init__(self, movielens_id: str, tmdb_id: str, imdb_id: str,
		title: str, year: int, runtime: int, genre: str, ave_rating: float,
		director: str, writer: str, description: str, cast: str, poster: str,
		count: int, rank: int, poster_identifier: str = ''):
		self.movielens_id = movielens_id
		self.tmdb_id = tmdb_id
		self.imdb_id = imdb_id
		self.title = title
		self.year = year
		self.runtime = runtime
		self.genre = genre
		self.ave_rating = ave_rating
		self.director = director
		self.writer = writer
		self.description = description
		self.cast = cast
		self.poster = poster
		self.count = count
		self.rank = rank
		self.poster_identifier = poster_identifier
