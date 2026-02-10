"""clean moviedb schema

Revision ID: 466ae1376c9e
Revises:
Create Date: 2026-02-03 12:54:19.723655

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '466ae1376c9e'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'movies',
        sa.Column('movielens_id', sa.String(), nullable=False),
        sa.Column('tmdb_id', sa.String(), nullable=True),
        sa.Column('imdb_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('runtime', sa.Integer(), nullable=False),
        sa.Column('genre', sa.String(), nullable=False),
        sa.Column('imdb_genres', sa.String(), nullable=True),
        sa.Column('tmdb_genres', sa.String(), nullable=True),
        sa.Column('ave_rating', sa.Float(), nullable=False),
        sa.Column('imdb_avg_rating', sa.Float(), nullable=True),
        sa.Column('imdb_rate_count', sa.Integer(), nullable=True),
        sa.Column('tmdb_avg_rating', sa.Float(), nullable=True),
        sa.Column('tmdb_rate_count', sa.Integer(), nullable=True),
        sa.Column('movielens_avg_rating', sa.Float(), nullable=True),
        sa.Column('movielens_rate_count', sa.Integer(), nullable=True),
        sa.Column('origin_country', sa.String(), nullable=True),
        sa.Column('parental_guide', sa.String(), nullable=True),
        sa.Column('director', sa.Text(), nullable=False),
        sa.Column('writer', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('cast', sa.Text(), nullable=False),
        sa.Column('poster', sa.String(), nullable=False),
        sa.Column('tmdb_poster', sa.String(), nullable=True),
        sa.Column('count', sa.Integer(), nullable=False),
        sa.Column('rank', sa.Integer(), nullable=False),
        sa.Column('imdb_popularity', sa.Float(), nullable=True),
        sa.Column('tmdb_popularity', sa.Float(), nullable=True),
        sa.Column('poster_identifier', sa.String(), nullable=True),
        sa.Column('movie_lens_dataset', sa.String(), nullable=True),
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_movies')),
    )
    op.create_index(op.f('ix_movies_imdb_id'), 'movies', ['imdb_id'], unique=True)
    op.create_index(op.f('ix_movies_movielens_id'), 'movies', ['movielens_id'], unique=True)
    op.create_index(
        op.f('ix_movies_title'),
        'movies',
        ['title', 'description'],
        unique=False,
        postgresql_using='gin',
        postgresql_ops={'title': 'gin_trgm_ops', 'description': 'gin_trgm_ops'},
    )
    op.create_index(op.f('ix_movies_tmdb_id'), 'movies', ['tmdb_id'], unique=False)
    op.create_table(
        'movie_emotions',
        sa.Column('movielens_id', sa.String(), nullable=False),
        sa.Column('anger', sa.Float(), nullable=False),
        sa.Column('anticipation', sa.Float(), nullable=False),
        sa.Column('disgust', sa.Float(), nullable=False),
        sa.Column('fear', sa.Float(), nullable=False),
        sa.Column('joy', sa.Float(), nullable=False),
        sa.Column('surprise', sa.Float(), nullable=False),
        sa.Column('sadness', sa.Float(), nullable=False),
        sa.Column('trust', sa.Float(), nullable=False),
        sa.Column('iers_count', sa.Integer(), nullable=False),
        sa.Column('iers_rank', sa.Integer(), nullable=False),
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('movie_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], name=op.f('fk_movie_emotions_movie_id')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_movie_emotions')),
    )
    op.create_index(op.f('ix_movie_emotions_movie_id'), 'movie_emotions', ['movie_id'], unique=False)
    op.create_index(op.f('ix_movie_emotions_movielens_id'), 'movie_emotions', ['movielens_id'], unique=False)
    op.create_table(
        'movie_recommendation_text',
        sa.Column('formal', sa.Text(), nullable=False),
        sa.Column('informal', sa.Text(), nullable=False),
        sa.Column('source', sa.String(), nullable=True),
        sa.Column('model', sa.String(), nullable=True),
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('movie_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], name=op.f('fk_movie_recommendation_text_movie_id')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_movie_recommendation_text')),
    )
    op.create_index(
        op.f('ix_movie_recommendation_text_movie_id'), 'movie_recommendation_text', ['movie_id'], unique=False
    )
    op.create_table(
        'reviews',
        sa.Column('review_id', sa.String(), nullable=False),
        sa.Column('review_text', sa.Text(), nullable=False),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('movie_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], name=op.f('fk_reviews_movie_id')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_reviews')),
        sa.UniqueConstraint('review_id', name=op.f('uq_reviews_review_id')),
    )
    op.create_index(op.f('ix_reviews_movie_id'), 'reviews', ['movie_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_reviews_movie_id'), table_name='reviews')
    op.drop_table('reviews')
    op.drop_index(op.f('ix_movie_recommendation_text_movie_id'), table_name='movie_recommendation_text')
    op.drop_table('movie_recommendation_text')
    op.drop_index(op.f('ix_movie_emotions_movielens_id'), table_name='movie_emotions')
    op.drop_index(op.f('ix_movie_emotions_movie_id'), table_name='movie_emotions')
    op.drop_table('movie_emotions')
    op.drop_index(op.f('ix_movies_tmdb_id'), table_name='movies')
    op.drop_index(
        op.f('ix_movies_title'),
        table_name='movies',
        postgresql_using='gin',
        postgresql_ops={'title': 'gin_trgm_ops', 'description': 'gin_trgm_ops'},
    )
    op.drop_index(op.f('ix_movies_movielens_id'), table_name='movies')
    op.drop_index(op.f('ix_movies_imdb_id'), table_name='movies')
    op.drop_table('movies')
