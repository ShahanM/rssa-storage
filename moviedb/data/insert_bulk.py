from moviedb.dbconfig import DB_URI, session
from moviedb.schema import Movie, MovieEmotions, MovieRecommendationText
from typing import Union
import csv
import argparse

mydb = f'postgresql+psycopg2://{DB_URI}?client_encoding=utf8'

def map_row(_row, _names):
		return dict(zip(_names, _row))

def load_csv(file_path) -> list[dict[str, Union[str, int]]]:
	with open(file_path, 'r') as f:
		reader = csv.reader(f)
		header = next(reader)
		print(header)
		rows = list(reader)

		_data = [map_row(row, header) for row in rows]

	return _data


def insert_movies(movies):
	_movies = []
	for movieitem in movies:
		movie = Movie(
			movielens_id = movieitem['movie_id'], 
			tmdb_id = '', 
			imdb_id = movieitem['imdb_id'],
			title = movieitem['title'],
			year = movieitem['year'],
			runtime = movieitem['runtime'], 
			genre = movieitem['genre'],
			ave_rating = movieitem['aveRating'] if movieitem['aveRating'] else 0.0,
			director = movieitem['director'] if movieitem['director'] else '',
			writer = movieitem['writer'] if movieitem['writer'] else '',
			description = movieitem['description'],
			cast = movieitem['cast'] if movieitem['cast'] else '',
			poster = movieitem['poster'],
			count = movieitem['count'],
			rank = movieitem['rank']
		)
		_movies.append(movie)
	
	db = session()

	db.bulk_save_objects(_movies)
	db.commit()


def insert_emotions(emotions):
	_emotions = []
	db = session()
	dbmovies = {movie.movielens_id: movie.id for movie in db.query(Movie).all()}
	for emotionitem in emotions:
		emotion = MovieEmotions(
			movie_id=dbmovies[emotionitem['movie_id']],
			movielens_id=emotionitem['movie_id'],
			anger=emotionitem['anger'],
			anticipation=emotionitem['anticipation'],
			disgust=emotionitem['disgust'],
			fear=emotionitem['fear'],
			joy=emotionitem['joy'],
			surprise=emotionitem['surprise'],
			sadness=emotionitem['sadness'],
			trust=emotionitem['trust'],
			iers_count=emotionitem['ieRS_count'],
			iers_rank=emotionitem['ieRS_rank']
		)
		_emotions.append(emotion)
	db.bulk_save_objects(_emotions)
	db.commit()


def insert_recommendation_text(recommendations):
	_recommendations = []
	db = session()
	dbmovies = {movie.movielens_id: movie.id for movie in db.query(Movie).all()}
	for rec in recommendations:
		recommendation = MovieRecommendationText(
			movie_id=dbmovies[rec['movie_id']],
			formal=rec['formal_description'],
			informal=rec['informal_description']
		)
		_recommendations.append(recommendation)
	db.bulk_save_objects(_recommendations)
	db.commit()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Insert data from file to database')
	parser.add_argument('--file', type=str, help='Path to csv file')
	parser.add_argument('--table', type=str, help='Name of table to insert data into')
	args = parser.parse_args()

	data = load_csv(args.file)
	if args.table == 'movies':
		insert_movies(data)
	elif args.table == 'emotions':
		insert_emotions(data)
	elif args.table == 'recommendations':
		insert_recommendation_text(data)
	else:
		print('Invalid table name')
		exit(1)

