from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
character = Table('character', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('character_id', INTEGER),
    Column('firstname', VARCHAR(length=255)),
    Column('lastname', VARCHAR(length=255)),
    Column('nickname', VARCHAR(length=255)),
    Column('age', INTEGER),
    Column('gender', VARCHAR(length=255)),
    Column('birthday', DATE),
    Column('sign', VARCHAR(length=255)),
    Column('sexual', VARCHAR(length=255)),
    Column('occup', VARCHAR(length=255)),
    Column('residence', VARCHAR(length=255)),
    Column('height', VARCHAR(length=255)),
    Column('weight', VARCHAR(length=255)),
    Column('hair', VARCHAR(length=255)),
    Column('eyes', VARCHAR(length=255)),
    Column('status', VARCHAR(length=255)),
    Column('likes', VARCHAR(length=255)),
    Column('dislikes', VARCHAR(length=255)),
    Column('person', TEXT),
    Column('appear', TEXT),
    Column('about', TEXT),
    Column('headcanon', TEXT),
    Column('fandom', VARCHAR(length=255)),
    Column('theme', VARCHAR(length=255)),
    Column('url', VARCHAR(length=255)),
    Column('img', VARCHAR(length=255)),
    Column('created', TIMESTAMP),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['character'].columns['url'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['character'].columns['url'].create()
