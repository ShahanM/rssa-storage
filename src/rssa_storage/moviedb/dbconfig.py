import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Load environment variables from .env file
load_dotenv()


dbuser = os.getenv("DB_USER")
if dbuser is None:
    raise ValueError("DB_USER environment variable is not set")

dbpass = os.getenv("DB_PASSWORD")
if dbpass is None:
    raise ValueError("DB_PASSWORD environment variable is not set")

dbhost = os.getenv("DB_HOST")
if dbhost is None:
    raise ValueError("DB_HOST environment variable is not set")

dbport = os.getenv("DB_PORT")
if dbport is None:
    raise ValueError("DB_PORT environment variable is not set")

dbname = os.getenv("DB_NAME")
if dbname is None:
    raise ValueError("DB_NAME environment variable is not set")


# Remember to add the protocol and encoding
DB_URI = f"{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}"

engine = create_engine(f'postgresql+psycopg2://{DB_URI}?client_encoding=utf8')
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
	db = session()
	try:
		yield db
	finally:
		db.close()

Base = declarative_base()