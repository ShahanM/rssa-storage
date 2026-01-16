"""add a short_code column to StudyConditions

Revision ID: fe1da9b7a44f
Revises: a587b7ffa799
Create Date: 2026-01-09 03:07:02.470840

"""

import random
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'fe1da9b7a44f'
down_revision: str | None = 'a587b7ffa799'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

ADJECTIVES = [
    'Amaranth',
    'Vermilion',
    'Crimson',
    'Scarlet',
    'Coral',
    'Peach',
    'Saffron',
    'Amber',
    'Russet',
    'Maroon',
    'Citrine',
    'Gold',
    'Ivory',
    'Lime',
    'Chartreuse',
    'Emerald',
    'Viridian',
    'Jade',
    'Sage',
    'Olive',
    'Teal',
    'Cyan',
    'Azure',
    'Cobalt',
    'Indigo',
    'Sapphire',
    'Cerulean',
    'Slate',
    'Navy',
    'Midnight',
    'Lavender',
    'Mauve',
    'Violet',
    'Amethyst',
    'Plum',
    'Orchid',
    'Magenta',
    'Fuchsia',
    'Byzantium',
    'Lilac',
    'Silver',
    'Platinum',
    'Obsidian',
    'Charcoal',
    'Ebony',
    'Onyx',
    'Pearl',
    'Bronze',
    'Copper',
    'Umber',
]

NOUNS = [
    'Badger',
    'Bison',
    'Cheetah',
    'Dolphin',
    'Elk',
    'Fox',
    'Gazelle',
    'Ibex',
    'Jaguar',
    'Koala',
    'Lemur',
    'Lynx',
    'Marmot',
    'Narwhal',
    'Ocelot',
    'Otter',
    'Panda',
    'Pangolin',
    'Quokka',
    'Wolf',
    'Crane',
    'Eagle',
    'Falcon',
    'Hawk',
    'Heron',
    'Jay',
    'Kestrel',
    'Lark',
    'Owl',
    'Penguin',
    'Raven',
    'Starling',
    'Swan',
    'Swift',
    'Toucan',
    'Wren',
    'Axolotl',
    'Cobra',
    'Gecko',
    'Iguana',
    'Manta',
    'Newt',
    'Python',
    'Shark',
    'Turtle',
    'Viper',
    'Beetle',
    'Mantis',
    'Moth',
    'Wasp',
]


def generate_code():
    return f'{random.choice(ADJECTIVES)}-{random.choice(NOUNS)}'


def upgrade() -> None:
    op.add_column('study_conditions', sa.Column('short_code', sa.String(length=48), nullable=True))
    connection = op.get_bind()
    results = connection.execute(sa.text('SELECT id, study_id FROM study_conditions'))

    assigned_pairs = set()

    for row in results:
        attempt_count = 0
        while True:
            new_code = generate_code()

            if (row.study_id, new_code) not in assigned_pairs:
                assigned_pairs.add((row.study_id, new_code))
                break

            # Collision detected: simple retry
            attempt_count += 1
            if attempt_count > 100:
                new_code = f'{new_code}-{attempt_count}'
                assigned_pairs.add((row.study_id, new_code))
                break

        connection.execute(
            sa.text('UPDATE study_conditions SET short_code = :code WHERE id = :id'), {'code': new_code, 'id': row.id}
        )
    op.alter_column('study_conditions', 'short_code', nullable=False)
    op.create_unique_constraint(
        op.f('uq_study_conditions_study_id_short_code'),
        'study_conditions',
        ['study_id', 'short_code'],
        deferrable=True,
        initially='DEFERRED',
    )


def downgrade() -> None:
    op.drop_constraint(op.f('uq_study_conditions_study_id_short_code'), 'study_conditions', type_='unique')
    op.drop_column('study_conditions', 'short_code')
