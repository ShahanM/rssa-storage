#!/bin/bash
set -e

DB_URL="postgresql://rssa_dev:devpassword@rssa_postgres:5432/moviedb"
DATA_DIR="/app/data/seed_data"
S3_BASE_URL="https://rssa-models.s3.amazonaws.com/seed_data"

echo "Starting Dataset Ingestion"

mkdir -p $DATA_DIR

echo "Checking for golden dataset files..."

download_if_missing() {
    local filename=$1
    if [ ! -f "$DATA_DIR/$filename" ]; then
        echo "Downloading $filename from S3..."
        curl -f -sS -o "$DATA_DIR/$filename" "$S3_BASE_URL/$filename"
    else
        echo "$filename already exists. Skipping download."
    fi
}

download_if_missing "local_movies.csv"
download_if_missing "local_movie_emotions.csv"
download_if_missing "local_movie_recommendation_text.csv"
download_if_missing "sliced_movielens_ratings.csv"
download_if_missing "sliced_ieRS_emotions_g20.csv"

echo "Clearing existing data..."
psql $DB_URL -c "TRUNCATE TABLE movies CASCADE;"

echo "Ingesting base movies..."
psql $DB_URL -c "\copy movies (id, movielens_id, tmdb_id, imdb_id, title, year, runtime, genre, imdb_genres, tmdb_genres, ave_rating, imdb_avg_rating, imdb_rate_count, tmdb_avg_rating, tmdb_rate_count, movielens_avg_rating, movielens_rate_count, origin_country, parental_guide, director, writer, description, \"cast\", poster, tmdb_poster, count, rank, imdb_popularity, tmdb_popularity, poster_identifier, movie_lens_dataset) FROM '$DATA_DIR/local_movies.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL '\N', FORCE_NOT_NULL (director, writer, description, \"cast\"));"

if [ -f "$DATA_DIR/local_movie_emotions.csv" ]; then
    echo "Ingesting movie emotions..."
    psql $DB_URL -c "\copy movie_emotions (id, movie_id, movielens_id, anger, anticipation, disgust, fear, joy, surprise, sadness, trust, iers_count, iers_rank) FROM '$DATA_DIR/local_movie_emotions.csv' WITH (FORMAT csv, HEADER true, NULL '\N');"
fi

if [ -f "$DATA_DIR/local_movie_recommendation_text.csv" ]; then
    echo "Ingesting recommendation texts..."
    psql $DB_URL -c "\copy movie_recommendation_text (id, movie_id, formal, informal, source, model) FROM '$DATA_DIR/local_movie_recommendation_text.csv' WITH (FORMAT csv, HEADER true, NULL '\N');"
fi

if [ -f "$DATA_DIR/local_reviews.csv" ]; then
    echo "Ingesting reviews..."
    psql $DB_URL -c "\copy reviews (id, movie_id, review_id, review_text, source) FROM '$DATA_DIR/local_reviews.csv' WITH (FORMAT csv, HEADER true, NULL '\N');"
fi

echo "Moviedb Seeding Complete"
