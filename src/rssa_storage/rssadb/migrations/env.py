# import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from rssa_storage.rssadb.models import Base
from rssa_storage.shared.db_base import create_db_url

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

db_url = create_db_url(env_prefix='RSSA_DB', is_async=False, use_neon=True)
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


# FIXME: Temporary to clean database
# Keeping this here for now while I still debug a few things
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
        return name in target_tables

    if hasattr(object, 'table') and object.table is not None:
        return object.table.name in target_tables

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
