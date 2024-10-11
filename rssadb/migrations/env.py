from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

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

config.set_main_option("sqlalchemy.url", f"postgresql://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}")

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()