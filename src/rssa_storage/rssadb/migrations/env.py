# import sys
from logging.config import fileConfig

# from pathlib import Path
from alembic import context

# from dbconfig import Base
from sqlalchemy import engine_from_config, pool

from rssa_storage.rssadb.db_base import create_db_url
from rssa_storage.rssadb.models import Base

# current_file = Path(__file__).resolve()
# repo_root = current_file.parents[3]
# sys.path.append(str(repo_root))
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

db_url = create_db_url(False)
config.set_main_option('sqlalchemy.url', db_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


# TODO: Temporary to clean database
def include_object(object, name, type_, reflected, compare_to):
    # Only process objects meant for these specific tables
    target_tables = [
        'studies',
        'study_conditions',
        'study_steps',
        'study_step_pages',
        'study_step_page_contents',
        'api_keys',
        'users',
        'study_participant_types',
        'study_participants',
        'participant_demographics',
        'participant_study_sessions',
        'participant_recommendation_contexts',
        'survey_items',
        'survey_constructs',
        'survey_scales',
        'survey_scale_levels',
        'pre_shuffled_movie_lists',
        'study_participant_movie_sessions',
        'feedbacks',
        'participant_survey_responses',
        'participant_freeform_responses',
        'participant_ratings',
        'participant_interaction_logs',
        'participant_study_interaction_responses',
    ]

    if type_ == 'table':
        # If true, Alembic processes this table. If false, it ignores it completely.
        return name in target_tables

    # Optional: If you want to be strict about columns/indexes belonging to those tables:
    if hasattr(object, 'table') and object.table is not None:
        return object.table.name in target_tables

    # Default to True for other types (like sequences) or let them pass if unsure
    return True


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            # include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
