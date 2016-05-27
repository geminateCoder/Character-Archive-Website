from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
character = Table('character', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('username', VARCHAR(length=255)),
    Column('firstname', VARCHAR(length=255)),
    Column('lastname', VARCHAR(length=255)),
    Column('img', VARCHAR(length=255)),
    Column('created', TIMESTAMP),
)

character = Table('character', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('character_id', Integer),
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
    pre_meta.tables['character'].columns['username'].drop()
    post_meta.tables['character'].columns['about'].create()
    post_meta.tables['character'].columns['age'].create()
    post_meta.tables['character'].columns['appear'].create()
    post_meta.tables['character'].columns['birthday'].create()
    post_meta.tables['character'].columns['character_id'].create()
    post_meta.tables['character'].columns['dislikes'].create()
    post_meta.tables['character'].columns['eyes'].create()
    post_meta.tables['character'].columns['fandom'].create()
    post_meta.tables['character'].columns['gender'].create()
    post_meta.tables['character'].columns['hair'].create()
    post_meta.tables['character'].columns['headcanon'].create()
    post_meta.tables['character'].columns['height'].create()
    post_meta.tables['character'].columns['likes'].create()
    post_meta.tables['character'].columns['nickname'].create()
    post_meta.tables['character'].columns['occup'].create()
    post_meta.tables['character'].columns['person'].create()
    post_meta.tables['character'].columns['residence'].create()
    post_meta.tables['character'].columns['sexual'].create()
    post_meta.tables['character'].columns['sign'].create()
    post_meta.tables['character'].columns['status'].create()
    post_meta.tables['character'].columns['theme'].create()
    post_meta.tables['character'].columns['url'].create()
    post_meta.tables['character'].columns['user_id'].create()
    post_meta.tables['character'].columns['weight'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['character'].columns['username'].create()
    post_meta.tables['character'].columns['about'].drop()
    post_meta.tables['character'].columns['age'].drop()
    post_meta.tables['character'].columns['appear'].drop()
    post_meta.tables['character'].columns['birthday'].drop()
    post_meta.tables['character'].columns['character_id'].drop()
    post_meta.tables['character'].columns['dislikes'].drop()
    post_meta.tables['character'].columns['eyes'].drop()
    post_meta.tables['character'].columns['fandom'].drop()
    post_meta.tables['character'].columns['gender'].drop()
    post_meta.tables['character'].columns['hair'].drop()
    post_meta.tables['character'].columns['headcanon'].drop()
    post_meta.tables['character'].columns['height'].drop()
    post_meta.tables['character'].columns['likes'].drop()
    post_meta.tables['character'].columns['nickname'].drop()
    post_meta.tables['character'].columns['occup'].drop()
    post_meta.tables['character'].columns['person'].drop()
    post_meta.tables['character'].columns['residence'].drop()
    post_meta.tables['character'].columns['sexual'].drop()
    post_meta.tables['character'].columns['sign'].drop()
    post_meta.tables['character'].columns['status'].drop()
    post_meta.tables['character'].columns['theme'].drop()
    post_meta.tables['character'].columns['url'].drop()
    post_meta.tables['character'].columns['user_id'].drop()
    post_meta.tables['character'].columns['weight'].drop()
