"""Centralized Database components for asynchronous operations."""

import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

load_dotenv()


def create_db_url(env_prefix: str, is_async: bool = False, use_neon: bool = False) -> str:
    """
    Creates a database URL dynamically based on an environment variable prefix.

    Args:
        env_prefix: The prefix for your env vars (e.g., 'RSSA_DB', 'MOVIE_DB')
        is_async: If True, uses asyncpg. If False, uses psycopg2.
        use_neon: If True, appends Neon-specific SSL parameters.
    """
    dbuser = os.environ.get(f'{env_prefix}_USER', os.environ.get('PGUSER', ''))
    dbpass = os.environ.get(f'{env_prefix}_PASSWORD', os.environ.get('PGPASSWORD', ''))
    dbhost = os.environ.get(f'{env_prefix}_HOST', os.environ.get('PGHOST', ''))
    dbname = os.environ.get(f'{env_prefix}_NAME', os.environ.get('PGDATABASE', ''))

    driver = 'asyncpg' if is_async else 'psycopg2'

    if use_neon:
        sslmode = os.environ.get(f'{env_prefix}_SSLMODE', os.environ.get('PGSSLMODE', 'require'))
        channel = os.environ.get(f'{env_prefix}_CHANNELBINDING', os.environ.get('PGCHANNELBINDING', ''))

        param = f'sslmode={sslmode}'
        if channel:
            param += f'&channel_binding={channel}'

        return f'postgresql+{driver}://{dbuser}:{dbpass}@{dbhost}/{dbname}?{param}'
    else:
        dbport = os.environ.get(f'{env_prefix}_PORT', os.environ.get('DB_PORT', '5432'))
        host_port = f'{dbhost}:{dbport}' if dbport else dbhost
        return f'postgresql+{driver}://{dbuser}:{dbpass}@{host_port}/{dbname}'


def create_db_components(
    env_prefix: str, use_neon: bool = False, echo: bool = False
) -> tuple[AsyncEngine, async_sessionmaker]:
    """Creates the async engine and session factory for FastAPI."""
    db_url = create_db_url(env_prefix=env_prefix, is_async=True, use_neon=use_neon)

    engine = create_async_engine(db_url, echo=echo)
    session_factory = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

    return engine, session_factory
