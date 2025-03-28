from dbconfig import Base
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa
import uuid
from datetime import datetime, timezone
from typing import Any


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

	imdb_genres = sa.Column(sa.String, nullable=True)
	tmdb_genres = sa.Column(sa.String, nullable=True)
	
	ave_rating = sa.Column(sa.Numeric[Any], nullable=False)
	
	imdb_avg_rating = sa.Column(sa.Numeric[Any], nullable=True)
	imdb_rate_count = sa.Column(sa.Integer, nullable=True)

	tmdb_avg_rating = sa.Column(sa.Numeric[Any], nullable=True)
	tmdb_rate_count = sa.Column(sa.Integer, nullable=True)

	movielens_avg_rating = sa.Column(sa.Numeric[Any], nullable=True)
	movielens_rate_count = sa.Column(sa.Integer, nullable=True)

	origin_country = sa.Column(sa.String, nullable=True)
	
	parental_guide = sa.Column(sa.String, nullable=True)

	movie_lens_dataset = sa.Column(sa.String, nullable=True)
	last_updated = sa.Column(sa.DateTime, nullable=True)
	
	director = sa.Column(sa.Text, nullable=False)
	writer = sa.Column(sa.Text, nullable=False)
	description = sa.Column(sa.Text, nullable=False)
	cast = sa.Column(sa.Text, nullable=False)

	poster = sa.Column(sa.String, nullable=False)
	tmdb_poster = sa.Column(sa.String, nullable=True)
	
	count = sa.Column(sa.Integer, nullable=False)
	
	rank = sa.Column(sa.Integer, nullable=False)

	imdb_popularity = sa.Column(sa.Numeric[Any], nullable=True)
	tmdb_popularity = sa.Column(sa.Numeric[Any], nullable=True)
	
	poster_identifier = sa.Column(sa.String, nullable=True)

	# All required fields are part of the Movielens dataset
	# All other fields need to be updated from TMDB and IMDB
	def __init__(self, 
		movielens_id: str, # required
		imdb_id: str, # required
		title: str, # required
		year: int, # required
		genre: str, # required
		runtime: int = 0,
		ave_rating: float = 0,
		director: str = '',
		writer: str = '',
		description: str = '',
		cast: str = '',
		poster: str = '',
		count: int = -1,
		rank: int = -1,
		poster_identifier: str = ''):

		self.movielens_id = movielens_id
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
		self.last_updated = datetime.now(timezone.utc)
