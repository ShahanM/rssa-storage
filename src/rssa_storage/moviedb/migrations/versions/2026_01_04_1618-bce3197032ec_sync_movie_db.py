"""Sync movie db

Revision ID: bce3197032ec
Revises: a9809eded74e
Create Date: 2026-01-04 16:18:15.227911

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bce3197032ec'
down_revision: str | None = 'a9809eded74e'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    ################
    # MovieEmotion #
    ################
    # Add the date audit columns
    op.add_column(
        'movie_emotions',
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.add_column(
        'movie_emotions',
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # Alter all the emotions colums type from Numeric to Float
    op.alter_column('movie_emotions', 'anger', existing_type=sa.NUMERIC(), type_=sa.Float(), existing_nullable=False)
    op.alter_column(
        'movie_emotions', 'anticipation', existing_type=sa.NUMERIC(), type_=sa.Float(), existing_nullable=False
    )
    op.alter_column('movie_emotions', 'disgust', existing_type=sa.NUMERIC(), type_=sa.Float(), existing_nullable=False)
    op.alter_column('movie_emotions', 'fear', existing_type=sa.NUMERIC(), type_=sa.Float(), existing_nullable=False)
    op.alter_column('movie_emotions', 'joy', existing_type=sa.NUMERIC(), type_=sa.Float(), existing_nullable=False)
    op.alter_column('movie_emotions', 'surprise', existing_type=sa.NUMERIC(), type_=sa.Float(), existing_nullable=False)
    op.alter_column('movie_emotions', 'sadness', existing_type=sa.NUMERIC(), type_=sa.Float(), existing_nullable=False)
    op.alter_column('movie_emotions', 'trust', existing_type=sa.NUMERIC(), type_=sa.Float(), existing_nullable=False)

    # We don't want movie_emotion entries to be unique, we will pick the latest
    op.drop_constraint(op.f('movie_emotions_movie_id_key'), 'movie_emotions', type_='unique')

    op.drop_index(op.f('movielens_emotions_id_idx'), table_name='movie_emotions')
    op.create_index(op.f('ix_movie_emotions_movie_id'), 'movie_emotions', ['movie_id'], unique=False)
    op.create_index(op.f('ix_movie_emotions_movielens_id'), 'movie_emotions', ['movielens_id'], unique=False)

    ###########################
    # MovieRecommendationText #
    ###########################
    # This is not a used index and does not conform to naming convention
    op.drop_index(op.f('movie_recommendation_text_id_idx'), table_name='movie_recommendation_text')

    #########
    # Movie #
    #########
    # Add the date audit columns
    op.add_column(
        'movies', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )
    op.add_column(
        'movies', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )

    # Alter all Numeric columns to Float, we do not need that kind of precision
    op.alter_column('movies', 'ave_rating', existing_type=sa.NUMERIC(), type_=sa.Float(), existing_nullable=False)
    op.alter_column('movies', 'imdb_avg_rating', existing_type=sa.NUMERIC(), type_=sa.Float(), existing_nullable=True)
    op.alter_column('movies', 'tmdb_avg_rating', existing_type=sa.NUMERIC(), type_=sa.Float(), existing_nullable=True)
    op.alter_column(
        'movies', 'movielens_avg_rating', existing_type=sa.NUMERIC(), type_=sa.Float(), existing_nullable=True
    )
    op.alter_column('movies', 'imdb_popularity', existing_type=sa.NUMERIC(), type_=sa.Float(), existing_nullable=True)
    op.alter_column('movies', 'tmdb_popularity', existing_type=sa.NUMERIC(), type_=sa.Float(), existing_nullable=True)

    # We have an alternate way to handle posters, this can be nullable
    op.alter_column('movies', 'poster_identifier', existing_type=sa.VARCHAR(), nullable=True)

    # Rename index, and create new indexes
    op.drop_index(
        op.f('idx_movie_title_trgm'),
        table_name='movies',
        postgresql_ops={'title': 'gin_trgm_ops'},
        postgresql_using='gin',
    )
    op.drop_index(op.f('imdb_id_idx'), table_name='movies')
    op.drop_index(op.f('movielens_id_idx'), table_name='movies')
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

    # We are replacing the last_updated with updated_at, since all entries will have a new updated date we can drop this
    op.drop_column('movies', 'last_updated')

    ##########
    # Review #
    ##########
    # Add the date audit columns
    op.add_column(
        'reviews', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )
    op.add_column(
        'reviews', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False)
    )

    # Alter the id from BIGINT to UUID as per convention
    op.drop_constraint('reviews_pkey', 'reviews', type_='primary')
    op.drop_column('reviews', 'id')
    op.add_column('reviews', sa.Column('id', sa.UUID(), nullable=False, server_default=sa.text('gen_random_uuid()')))
    op.create_primary_key('pk_reviews', 'reviews', ['id'])

    # Rename constraint key
    op.drop_constraint(op.f('uq_review_id'), 'reviews', type_='unique')
    op.create_unique_constraint(op.f('uq_reviews_review_id'), 'reviews', ['review_id'])

    # Rename foreign key to match naming convention
    op.drop_constraint(op.f('reviews_movie_id_fkey'), 'reviews', type_='foreignkey')
    op.create_foreign_key(op.f('fk_reviews_movie_id'), 'reviews', 'movies', ['movie_id'], ['id'])

    # We replcaed the scraped_at with created_at
    op.drop_column('reviews', 'scraped_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'reviews',
        sa.Column(
            'scraped_at',
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_constraint(op.f('fk_reviews_movie_id'), 'reviews', type_='foreignkey')
    op.create_foreign_key(op.f('reviews_movie_id_fkey'), 'reviews', 'movies', ['movie_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(op.f('uq_reviews_review_id'), 'reviews', type_='unique')
    op.create_unique_constraint(op.f('uq_review_id'), 'reviews', ['review_id'], postgresql_nulls_not_distinct=False)

    op.drop_constraint('pk_reviews', 'reviews', type_='primary')
    op.drop_column('reviews', 'id')
    op.add_column('reviews', sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False))
    op.create_primary_key('reviews_pkey', 'reviews', ['id'])

    op.drop_column('reviews', 'updated_at')
    op.drop_column('reviews', 'created_at')
    op.add_column('movies', sa.Column('last_updated', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_movies_tmdb_id'), table_name='movies')
    op.drop_index(
        op.f('ix_movies_title'),
        table_name='movies',
        postgresql_using='gin',
        postgresql_ops={'title': 'gin_trgm_ops', 'description': 'gin_trgm_ops'},
    )
    op.drop_index(op.f('ix_movies_movielens_id'), table_name='movies')
    op.drop_index(op.f('ix_movies_imdb_id'), table_name='movies')
    op.create_index(op.f('movielens_id_idx'), 'movies', ['movielens_id'], unique=True)
    op.create_index(op.f('imdb_id_idx'), 'movies', ['imdb_id'], unique=True)
    op.create_index(
        op.f('idx_movie_title_trgm'),
        'movies',
        ['title'],
        unique=False,
        postgresql_ops={'title': 'gin_trgm_ops'},
        postgresql_using='gin',
    )
    op.alter_column('movies', 'poster_identifier', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('movies', 'tmdb_popularity', existing_type=sa.Float(), type_=sa.NUMERIC(), existing_nullable=True)
    op.alter_column('movies', 'imdb_popularity', existing_type=sa.Float(), type_=sa.NUMERIC(), existing_nullable=True)
    op.alter_column(
        'movies', 'movielens_avg_rating', existing_type=sa.Float(), type_=sa.NUMERIC(), existing_nullable=True
    )
    op.alter_column('movies', 'tmdb_avg_rating', existing_type=sa.Float(), type_=sa.NUMERIC(), existing_nullable=True)
    op.alter_column('movies', 'imdb_avg_rating', existing_type=sa.Float(), type_=sa.NUMERIC(), existing_nullable=True)
    op.alter_column('movies', 'ave_rating', existing_type=sa.Float(), type_=sa.NUMERIC(), existing_nullable=False)
    op.drop_column('movies', 'updated_at')
    op.drop_column('movies', 'created_at')
    op.create_index(op.f('movie_recommendation_text_id_idx'), 'movie_recommendation_text', ['movie_id'], unique=True)
    op.drop_index(op.f('ix_movie_emotions_movielens_id'), table_name='movie_emotions')
    op.drop_index(op.f('ix_movie_emotions_movie_id'), table_name='movie_emotions')
    op.create_index(op.f('movielens_emotions_id_idx'), 'movie_emotions', ['movielens_id'], unique=True)
    op.create_unique_constraint(
        op.f('movie_emotions_movie_id_key'), 'movie_emotions', ['movie_id'], postgresql_nulls_not_distinct=False
    )
    op.alter_column('movie_emotions', 'trust', existing_type=sa.Float(), type_=sa.NUMERIC(), existing_nullable=False)
    op.alter_column('movie_emotions', 'sadness', existing_type=sa.Float(), type_=sa.NUMERIC(), existing_nullable=False)
    op.alter_column('movie_emotions', 'surprise', existing_type=sa.Float(), type_=sa.NUMERIC(), existing_nullable=False)
    op.alter_column('movie_emotions', 'joy', existing_type=sa.Float(), type_=sa.NUMERIC(), existing_nullable=False)
    op.alter_column('movie_emotions', 'fear', existing_type=sa.Float(), type_=sa.NUMERIC(), existing_nullable=False)
    op.alter_column('movie_emotions', 'disgust', existing_type=sa.Float(), type_=sa.NUMERIC(), existing_nullable=False)
    op.alter_column(
        'movie_emotions', 'anticipation', existing_type=sa.Float(), type_=sa.NUMERIC(), existing_nullable=False
    )
    op.alter_column('movie_emotions', 'anger', existing_type=sa.Float(), type_=sa.NUMERIC(), existing_nullable=False)
    op.drop_column('movie_emotions', 'updated_at')
    op.drop_column('movie_emotions', 'created_at')
    # ### end Alembic commands ###
