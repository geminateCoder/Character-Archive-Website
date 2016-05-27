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
    Column('img', VARCHAR(length=255)),
    Column('created', TIMESTAMP),
)

character = Table('character', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=255)),
    Column('firstname', String(length=255), default=ColumnDefault('')),
    Column('lastname', String(length=255), default=ColumnDefault('')),
    Column('nickname', String(length=255)),
    Column('age', Integer),
    Column('gender', String(length=255)),
    Column('birthday', Date),
    Column('sign', String(length=255)),
    Column('sexual', String(length=255)),
    Column('occup', String(length=255)),
    Column('residence', String(length=255)),
    Column('height', String(length=255)),
    Column('weight', String(length=255)),
    Column('hair', String(length=255)),
    Column('eyes', String(length=255)),
    Column('status', String(length=255)),
    Column('likes', String(length=255)),
    Column('dislikes', String(length=255)),
    Column('person', Text),
    Column('appear', Text),
    Column('about', Text),
    Column('headcanon', Text),
    Column('fandom', String(length=255)),
    Column('theme', String(length=255)),
    Column('url', String(length=255)),
    Column('img', String(length=255), default=ColumnDefault('/static/img/default_image.png')),
    Column('created', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['character'].columns['character_id'].drop()
    pre_meta.tables['character'].columns['user_id'].drop()
    post_meta.tables['character'].columns['url'].create()
    post_meta.tables['character'].columns['username'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['character'].columns['character_id'].create()
    pre_meta.tables['character'].columns['user_id'].create()
    post_meta.tables['character'].columns['url'].drop()
    post_meta.tables['character'].columns['username'].drop()
