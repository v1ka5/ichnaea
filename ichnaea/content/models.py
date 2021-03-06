from sqlalchemy import (
    Column,
    Date,
    SmallInteger,
    Unicode,
    UniqueConstraint,
)
from sqlalchemy.dialects.mysql import INTEGER as Integer

from ichnaea.db import _Model

STAT_TYPE = {
    '': -1,
    'location': 0,
    'cell': 1,
    'unique_cell': 2,
    'wifi': 3,
    'unique_wifi': 4,
}
STAT_TYPE_INVERSE = dict((v, k) for k, v in STAT_TYPE.items())

MAPSTAT_TYPE = {
    'location': 0,
}
MAPSTAT_TYPE_INVERSE = dict((v, k) for k, v in MAPSTAT_TYPE.items())


class MapStat(_Model):
    __tablename__ = 'mapstat'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }
    # lat/lon * 1000, so 12.345 is stored as 12345
    lat = Column(Integer, primary_key=True, autoincrement=False)
    lon = Column(Integer, primary_key=True, autoincrement=False)
    # mapped via MAPSTAT_TYPE
    key = Column(SmallInteger)
    value = Column(Integer(unsigned=True))

    def __init__(self, *args, **kw):
        if 'key' not in kw:
            kw['key'] = MAPSTAT_TYPE['location']
        super(MapStat, self).__init__(*args, **kw)

mapstat_table = MapStat.__table__


class Score(_Model):
    __tablename__ = 'score'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }

    id = Column(Integer(unsigned=True),
                primary_key=True, autoincrement=True)
    userid = Column(Integer(unsigned=True), index=True, unique=True)
    value = Column(Integer)

score_table = Score.__table__


class Stat(_Model):
    __tablename__ = 'stat'
    __table_args__ = (
        UniqueConstraint('key', 'time', name='stat_key_time_unique'),
        {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8',
        }
    )

    id = Column(Integer(unsigned=True),
                primary_key=True, autoincrement=True)
    # mapped via STAT_TYPE
    key = Column(SmallInteger)
    time = Column(Date)
    value = Column(Integer(unsigned=True))

    @property
    def name(self):
        return STAT_TYPE_INVERSE.get(self.key, '')

    @name.setter
    def name(self, value):
        self.key = STAT_TYPE[value]


stat_table = Stat.__table__


class User(_Model):
    __tablename__ = 'user'
    __table_args__ = (
        UniqueConstraint('nickname', name='user_nickname_unique'),
        {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8',
        }
    )

    id = Column(Integer(unsigned=True),
                primary_key=True, autoincrement=True)
    nickname = Column(Unicode(128))

user_table = User.__table__
