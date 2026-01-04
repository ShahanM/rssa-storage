"""Database base components for asynchronous operations."""

import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

load_dotenv()


def create_db_components(echo: bool = False) -> tuple[AsyncEngine, async_sessionmaker]:
    """Creates the async engine and session factory based on environment variables."""
    # dbuser = os.environ.get('DB_USER', '')
    # # dbuser = cfg.get_env_var('DB_USER')
    # dbpass = os.environ.get('DB_PASSWORD', '')
    # # dbpass = cfg.get_env_var('DB_PASSWORD')
    # dbhost = os.environ.get('DB_HOST', '')
    # # dbhost = cfg.get_env_var('DB_HOST')
    # dbport = os.environ.get('DB_PORT', '')
    # # dbport = cfg.get_env_var('DB_PORT')
    # dbname = os.environ.get('DB_NAME', '')
    # # dbname = cfg.get_env_var(db_name_env_key)

    # db_url = f'postgresql+asyncpg://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}'
    db_url = create_db_url(True)

    engine = create_async_engine(db_url, echo=echo)
    session_factory = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

    return engine, session_factory


def create_db_url(is_async: bool = False) -> str:
    dbuser = os.environ.get('DB_USER', '')
    # dbuser = cfg.get_env_var('DB_USER')
    dbpass = os.environ.get('DB_PASSWORD', '')
    # dbpass = cfg.get_env_var('DB_PASSWORD')
    dbhost = os.environ.get('DB_HOST', '')
    # dbhost = cfg.get_env_var('DB_HOST')
    dbport = os.environ.get('DB_PORT', '')
    # dbport = cfg.get_env_var('DB_PORT')
    dbname = os.environ.get('DB_NAME', '')
    # dbname = cfg.get_env_var(db_name_env_key)

    if is_async:
        return f'postgresql+asyncpg://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}'
    else:
        return f'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}'
