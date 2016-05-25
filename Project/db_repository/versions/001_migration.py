from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
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
    Column('original', Boolean, default=ColumnDefault(1)),
    Column('fandom', String(length=255)),
    Column('theme', String(length=255)),
    Column('url', String(length=255)),
    Column('img', String(length=255), default=ColumnDefault('/static/img/default_image.png')),
    Column('created', DateTime),
)

favorite = Table('favorite', post_meta,
    Column('user_id', Integer),
    Column('character_id', Integer),
)

follow = Table('follow', post_meta,
    Column('follower_id', Integer),
    Column('following_id', Integer),
)

post = Table('post', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=140)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
)

user_settings = Table('user_settings', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=255)),
    Column('displayname', String(length=255)),
    Column('age', Integer),
    Column('gender', String(length=255)),
    Column('sign', String(length=255)),
    Column('timezone', String(length=255)),
    Column('cpoints', Integer),
    Column('status', String(length=255)),
    Column('pref', String(length=255)),
    Column('exp', String(length=255)),
    Column('style', String(length=255)),
    Column('contact', String(length=255)),
    Column('about', Text),
    Column('img', String(length=255), default=ColumnDefault('/static/img/default_image.png')),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['character'].create()
    post_meta.tables['favorite'].create()
    post_meta.tables['follow'].create()
    post_meta.tables['post'].create()
    post_meta.tables['user_settings'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['character'].drop()
    post_meta.tables['favorite'].drop()
    post_meta.tables['follow'].drop()
    post_meta.tables['post'].drop()
    post_meta.tables['user_settings'].drop()
