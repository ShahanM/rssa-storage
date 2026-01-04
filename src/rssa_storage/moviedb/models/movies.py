from sqlalchemy import Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rssa_storage.moviedb.models.base import MovieBase, MovieForeignKeyMixin


class Movie(MovieBase):
    __tablename__ = 'movies'

    movielens_id: Mapped[str] = mapped_column(unique=True, index=True)

    # TMDB ID cannot be unique because of how IMDB movies are archived which influences the movielens_id
    tmdb_id: Mapped[str | None] = mapped_column(index=True)

    imdb_id: Mapped[str] = mapped_column(unique=True, index=True)

    title: Mapped[str] = mapped_column()
    year: Mapped[int] = mapped_column()
    runtime: Mapped[int] = mapped_column(default=0)
    genre: Mapped[str] = mapped_column()

    imdb_genres: Mapped[str | None] = mapped_column()
    tmdb_genres: Mapped[str | None] = mapped_column()

    ave_rating: Mapped[float] = mapped_column(default=0.0)

    imdb_avg_rating: Mapped[float | None] = mapped_column()
    imdb_rate_count: Mapped[int | None] = mapped_column()

    tmdb_avg_rating: Mapped[float | None] = mapped_column()
    tmdb_rate_count: Mapped[int | None] = mapped_column()

    movielens_avg_rating: Mapped[float | None] = mapped_column()
    movielens_rate_count: Mapped[int | None] = mapped_column()

    origin_country: Mapped[str | None] = mapped_column()

    parental_guide: Mapped[str | None] = mapped_column()

    director: Mapped[str] = mapped_column(Text, nullable=False, default='')
    writer: Mapped[str] = mapped_column(Text, nullable=False, default='')
    description: Mapped[str] = mapped_column(Text, nullable=False, default='')
    cast: Mapped[str] = mapped_column(Text, nullable=False)

    poster: Mapped[str] = mapped_column(default='')
    tmdb_poster: Mapped[str | None] = mapped_column()

    count: Mapped[int] = mapped_column(default=0)

    rank: Mapped[int] = mapped_column(default=-1)

    imdb_popularity: Mapped[float | None] = mapped_column()
    tmdb_popularity: Mapped[float | None] = mapped_column()

    poster_identifier: Mapped[str | None] = mapped_column()

    movie_lens_dataset: Mapped[str | None] = mapped_column()

    emotions: Mapped['MovieEmotions'] = relationship(
        'MovieEmotions',
        back_populates='movie',
        cascade='all, delete-orphan',
        uselist=False,
    )
    recommendations_text: Mapped['MovieRecommendationText'] = relationship(
        'MovieRecommendationText',
        back_populates='movie',
        cascade='all, delete-orphan',
        uselist=False,
    )
    reviews: Mapped['Review'] = relationship(
        'Review',
        back_populates='movie',
        cascade='all, delete-orphan',
        uselist=True,
        lazy=True,
    )

    __table_args__ = (
        Index(
            None,
            'title',
            postgresql_using='gin',
            postgresql_ops={'title': 'gin_trgm_ops'},
        ),
        Index(
            None,
            'title',
            'description',
            postgresql_using='gin',
            postgresql_ops={'title': 'gin_trgm_ops', 'description': 'gin_trgm_ops'},
        ),
    )


class MovieEmotions(MovieBase, MovieForeignKeyMixin):
    __tablename__ = 'movie_emotions'

    movielens_id: Mapped[str] = mapped_column(index=True)

    anger: Mapped[float] = mapped_column()
    anticipation: Mapped[float] = mapped_column()
    disgust: Mapped[float] = mapped_column()
    fear: Mapped[float] = mapped_column()
    joy: Mapped[float] = mapped_column()
    surprise: Mapped[float] = mapped_column()
    sadness: Mapped[float] = mapped_column()
    trust: Mapped[float] = mapped_column()

    iers_count: Mapped[int] = mapped_column()
    iers_rank: Mapped[int] = mapped_column()

    movie = relationship('Movie', back_populates='emotions')


class MovieRecommendationText(MovieBase, MovieForeignKeyMixin):
    __tablename__ = 'movie_recommendation_text'

    formal: Mapped[str] = mapped_column(Text)
    informal: Mapped[str] = mapped_column(Text)

    source: Mapped[str | None] = mapped_column()
    model: Mapped[str | None] = mapped_column()

    movie = relationship('Movie', back_populates='recommendations_text')


class Review(MovieBase, MovieForeignKeyMixin):
    __tablename__ = 'reviews'

    review_id: Mapped[str] = mapped_column(unique=True)
    review_text: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column()

    movie = relationship('Movie', back_populates='reviews')
