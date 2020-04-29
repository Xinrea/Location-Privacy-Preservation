# encoding=utf-8
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, REAL, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from GI.models.gridmap import GridMap


class Database:
    checkins = None
    csvs = None
    dbfilepath = None
    edges = None
    locdatetime_format = None
    name = None
    ranges = None
    tree_height = 6
    url = None


class SNAPBrightkite(Database):
    Base = declarative_base()
    edges = Table('edges',
                  Base.metadata,
                  Column('userid', Integer,
                         ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True,
                         index=True),
                  Column('friendid', Integer,
                         ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True,
                         index=True))

    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True, index=True)
        global_userid = Column(Integer, unique=True, index=True)

        followers = relationship('User',
                                 secondary='edges',
                                 primaryjoin='User.id==edges.c.userid',
                                 secondaryjoin='User.id==edges.c.friendid',
                                 back_populates='followees',
                                 passive_deletes=True)
        followees = relationship('User',
                                 secondary='edges',
                                 primaryjoin='User.id==edges.c.friendid',
                                 secondaryjoin='User.id==edges.c.userid',
                                 back_populates='followers',
                                 passive_deletes=True)
        locations = relationship('Location',
                                 secondary='checkins',
                                 primaryjoin='User.id==checkins.c.userid',
                                 secondaryjoin='checkins.c.locid==Location.id',
                                 back_populates='visitors',
                                 passive_deletes=True)
        checkins = relationship('Checkin',
                                back_populates='user',
                                passive_deletes=True)

    class Location(Base):
        __tablename__ = 'locations'
        # __table_args__ = (UniqueConstraint('lon', 'lat', name='gps'),)

        id = Column(Integer, primary_key=True, index=True)
        lon = Column(REAL, index=True)
        lat = Column(REAL, index=True)

        visitors = relationship('User',
                                secondary='checkins',
                                primaryjoin='Location.id==checkins.c.locid',
                                secondaryjoin='User.id==checkins.c.userid',
                                back_populates='locations',
                                passive_deletes=True)
        checkins = relationship('Checkin',
                                back_populates='location',
                                passive_deletes=True)

    class Checkin(Base):
        __tablename__ = 'checkins'

        id = Column(Integer, primary_key=True, autoincrement=True)
        userid = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
        locdatetime = Column(DateTime, index=True)
        locid = Column(Integer, ForeignKey('locations.id', ondelete='CASCADE'), index=True)

        user = relationship('User',
                            back_populates='checkins',
                            passive_deletes=True)
        location = relationship('Location',
                                back_populates='checkins',
                                passive_deletes=True)

    checkins = Checkin.__table__
    csvs = {'checkins': 'D:\\Workspace\\Datasets\\Location-Based Social Network\\SNAP Brightkite\\checkins.txt',
            'edges': 'D:\\Workspace\\Datasets\\Location-Based Social Network\\SNAP Brightkite\\edges.txt'}
    datetime_range = [datetime(2008, 3, 21, 20, 36, 21), datetime(2010, 10, 18, 18, 39, 58)]  # all datetimes
    name = 'SNAPBrightkite'
    dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\SNAP Brightkite\\' + name + '.db'
    locations = Location.__table__
    locdatetime_format = '%Y-%m-%d %H:%M:%S'
    ranges = [-180.0, 180.0, -80.0, 80.0]
    url = 'sqlite:///' + dbfilepath
    users = User.__table__


class SNAPBrightkite0201(SNAPBrightkite):
    Base = declarative_base()
    edges = Table('edges',
                  Base.metadata,
                  Column('userid', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
                         primary_key=True, index=True),
                  Column('friendid', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
                         primary_key=True, index=True))

    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True, index=True)
        global_userid = Column(Integer, unique=True, index=True)

        followers = relationship('User',
                                 secondary='edges',
                                 primaryjoin='User.id==edges.c.userid',
                                 secondaryjoin='User.id==edges.c.friendid',
                                 back_populates='followees',
                                 passive_deletes=True)
        followees = relationship('User',
                                 secondary='edges',
                                 primaryjoin='User.id==edges.c.friendid',
                                 secondaryjoin='User.id==edges.c.userid',
                                 back_populates='followers',
                                 passive_deletes=True)
        locations = relationship('Location',
                                 secondary='checkins',
                                 primaryjoin='User.id==checkins.c.userid',
                                 secondaryjoin='checkins.c.locid==Location.id',
                                 back_populates='visitors',
                                 passive_deletes=True)
        checkins = relationship('Checkin',
                                back_populates='user',
                                passive_deletes=True)

    class Location(Base):
        __tablename__ = 'locations'
        # __table_args__ = (UniqueConstraint('lon', 'lat', name='gps'),)

        id = Column(Integer, primary_key=True, index=True)

        visitors = relationship('User',
                                secondary='checkins',
                                primaryjoin='Location.id==checkins.c.locid',
                                secondaryjoin='User.id==checkins.c.userid',
                                back_populates='locations',
                                passive_deletes=True)
        checkins = relationship('Checkin',
                                back_populates='location',
                                passive_deletes=True)

    class Checkin(Base):
        __tablename__ = 'checkins'

        id = Column(Integer, primary_key=True)  # auto_increment=False
        userid = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
        locdatetime = Column(DateTime, index=True)
        lon = Column(REAL, index=True)
        lat = Column(REAL, index=True)
        locid = Column(Integer, ForeignKey('locations.id', ondelete='CASCADE'), index=True)
        gridlon = Column(Integer, index=True, nullable=True)  # new
        gridlat = Column(Integer, index=True, nullable=True)  # new
        gridid = Column(Integer, index=True, nullable=True)  # new
        clstlon = Column(REAL, index=True, nullable=True)  # new
        clstlat = Column(REAL, index=True, nullable=True)  # new
        clstid = Column(Integer, index=True, nullable=True)  # new

        user = relationship('User',
                            back_populates='checkins',
                            passive_deletes=True)
        location = relationship('Location',
                                back_populates='checkins',
                                passive_deletes=True)

    checkins = Checkin.__table__
    cluster_method = 'k-means'
    cluster_num = 100
    name = 'SNAPBrightkite0201'
    dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\SNAP Brightkite\\' + name + '.db'
    locations = Location.__table__
    min_tracelength = 20  # 1 means no filtering, 50 will keep more friends than 20!
    ranges = [-122.5153, -122.3789, 37.7084, 37.8130]  # San Francisco, 12km x 12km
    gridmap = GridMap(ranges=ranges, granularity=[0.005527, 0.004482])  # 500m x 500m
    subsample_rate = 1  # seconds, '1' or None means no subsampling
    timezone_offset = -7  # local time = UTC - 5 hours
    url = 'sqlite:///' + dbfilepath
    users = User.__table__


class SNAPBrightkite020101(SNAPBrightkite0201):
    checkins_super = SNAPBrightkite0201.checkins.name
    k_anonymity_method = 'EnhancedDLS'


class SNAPBrightkite02010103(SNAPBrightkite020101):
    K = 3
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020101.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0201010' + str(K)


class SNAPBrightkite02010104(SNAPBrightkite020101):
    K = 4
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020101.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0201010' + str(K)


class SNAPBrightkite02010105(SNAPBrightkite020101):
    K = 5
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020101.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0201010' + str(K)


class SNAPBrightkite02010106(SNAPBrightkite020101):
    K = 6
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020101.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0201010' + str(K)


class SNAPBrightkite02010107(SNAPBrightkite020101):
    K = 7
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020101.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0201010' + str(K)


class SNAPBrightkite02010108(SNAPBrightkite020101):
    K = 8
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020101.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0201010' + str(K)


class SNAPBrightkite02010109(SNAPBrightkite020101):
    K = 9
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020101.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0201010' + str(K)


class SNAPBrightkite02010110(SNAPBrightkite020101):
    K = 10
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020101.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020101' + str(K)


class SNAPBrightkite02010111(SNAPBrightkite020101):
    K = 11
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020101.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020101' + str(K)


class SNAPBrightkite02010112(SNAPBrightkite020101):
    K = 12
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020101.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020101' + str(K)


class SNAPBrightkite02010113(SNAPBrightkite020101):
    K = 13
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020101.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020101' + str(K)


class SNAPBrightkite02010114(SNAPBrightkite020101):
    K = 14
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020101.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020101' + str(K)


class SNAPBrightkite02010115(SNAPBrightkite020101):
    K = 15
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020101.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020101' + str(K)


class SNAPBrightkite02010116(SNAPBrightkite020101):
    K = 16
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020101.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020101' + str(K)


class SNAPBrightkite02010117(SNAPBrightkite020101):
    K = 17
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020101.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020101' + str(K)


class SNAPBrightkite02010118(SNAPBrightkite020101):
    K = 18
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020101.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020101' + str(K)


class SNAPBrightkite02010119(SNAPBrightkite020101):
    K = 19
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020101.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020101' + str(K)


class SNAPBrightkite02010120(SNAPBrightkite020101):
    K = 20
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020101.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020101' + str(K)


class SNAPBrightkite020102(SNAPBrightkite0201):
    checkins_super = SNAPBrightkite0201.checkins.name
    k_anonymity_method = 'EnhancedCADSA'
    max_cached_time = 3600


class SNAPBrightkite02010203(SNAPBrightkite020102):
    K = 3
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020102.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0201020' + str(K)


class SNAPBrightkite02010204(SNAPBrightkite020102):
    K = 4
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020102.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0201020' + str(K)


class SNAPBrightkite02010205(SNAPBrightkite020102):
    K = 5
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020102.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0201020' + str(K)


class SNAPBrightkite02010206(SNAPBrightkite020102):
    K = 6
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020102.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0201020' + str(K)


class SNAPBrightkite02010207(SNAPBrightkite020102):
    K = 7
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020102.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0201020' + str(K)


class SNAPBrightkite02010208(SNAPBrightkite020102):
    K = 8
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020102.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0201020' + str(K)


class SNAPBrightkite02010209(SNAPBrightkite020102):
    K = 9
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020102.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0201020' + str(K)


class SNAPBrightkite02010210(SNAPBrightkite020102):
    K = 10
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020102.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020102' + str(K)


class SNAPBrightkite02010211(SNAPBrightkite020102):
    K = 11
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020102.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020102' + str(K)


class SNAPBrightkite02010212(SNAPBrightkite020102):
    K = 12
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020102.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020102' + str(K)


class SNAPBrightkite02010213(SNAPBrightkite020102):
    K = 13
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020102.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020102' + str(K)


class SNAPBrightkite02010214(SNAPBrightkite020102):
    K = 14
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020102.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020102' + str(K)


class SNAPBrightkite02010215(SNAPBrightkite020102):
    K = 15
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020102.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020102' + str(K)


class SNAPBrightkite02010216(SNAPBrightkite020102):
    K = 16
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020102.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020102' + str(K)


class SNAPBrightkite02010217(SNAPBrightkite020102):
    K = 17
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020102.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020102' + str(K)


class SNAPBrightkite02010218(SNAPBrightkite020102):
    K = 18
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020102.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020102' + str(K)


class SNAPBrightkite02010219(SNAPBrightkite020102):
    K = 19
    checkins = '_'.join([SNAPBrightkite020101.checkins_super, SNAPBrightkite020102.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020102' + str(K)


class SNAPBrightkite02010220(SNAPBrightkite020102):
    K = 20
    checkins = '_'.join([SNAPBrightkite020102.checkins_super, SNAPBrightkite020102.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020102' + str(K)


class SNAPBrightkite0202(SNAPBrightkite0201):
    cluster_num = 200
    name = 'SNAPBrightkite0202'
    dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\SNAP Brightkite\\' + name + '.db'
    url = 'sqlite:///' + dbfilepath


class SNAPBrightkite020201(SNAPBrightkite0202):
    checkins_super = SNAPBrightkite0202.checkins.name
    k_anonymity_method = 'EnhancedDLS'


class SNAPBrightkite02020103(SNAPBrightkite020201):
    K = 3
    checkins = '_'.join([SNAPBrightkite020201.checkins_super, SNAPBrightkite020201.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0202010' + str(K)


class SNAPBrightkite02020104(SNAPBrightkite020201):
    K = 4
    checkins = '_'.join([SNAPBrightkite020201.checkins_super, SNAPBrightkite020201.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0202010' + str(K)


class SNAPBrightkite02020105(SNAPBrightkite020201):
    K = 5
    checkins = '_'.join([SNAPBrightkite020201.checkins_super, SNAPBrightkite020201.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0202010' + str(K)


class SNAPBrightkite02020106(SNAPBrightkite020201):
    K = 6
    checkins = '_'.join([SNAPBrightkite020201.checkins_super, SNAPBrightkite020201.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0202010' + str(K)


class SNAPBrightkite02020107(SNAPBrightkite020201):
    K = 7
    checkins = '_'.join([SNAPBrightkite020201.checkins_super, SNAPBrightkite020201.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0202010' + str(K)


class SNAPBrightkite02020108(SNAPBrightkite020201):
    K = 8
    checkins = '_'.join([SNAPBrightkite020201.checkins_super, SNAPBrightkite020201.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0202010' + str(K)


class SNAPBrightkite02020109(SNAPBrightkite020201):
    K = 9
    checkins = '_'.join([SNAPBrightkite020201.checkins_super, SNAPBrightkite020201.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0202010' + str(K)


class SNAPBrightkite02020110(SNAPBrightkite020201):
    K = 10
    checkins = '_'.join([SNAPBrightkite020201.checkins_super, SNAPBrightkite020201.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020201' + str(K)


class SNAPBrightkite02020111(SNAPBrightkite020201):
    K = 11
    checkins = '_'.join([SNAPBrightkite020201.checkins_super, SNAPBrightkite020201.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020201' + str(K)


class SNAPBrightkite02020112(SNAPBrightkite020201):
    K = 12
    checkins = '_'.join([SNAPBrightkite020201.checkins_super, SNAPBrightkite020201.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020201' + str(K)


class SNAPBrightkite02020113(SNAPBrightkite020201):
    K = 13
    checkins = '_'.join([SNAPBrightkite020201.checkins_super, SNAPBrightkite020201.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020201' + str(K)


class SNAPBrightkite02020114(SNAPBrightkite020201):
    K = 14
    checkins = '_'.join([SNAPBrightkite020201.checkins_super, SNAPBrightkite020201.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020201' + str(K)


class SNAPBrightkite02020115(SNAPBrightkite020201):
    K = 15
    checkins = '_'.join([SNAPBrightkite020201.checkins_super, SNAPBrightkite020201.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020201' + str(K)


class SNAPBrightkite02020116(SNAPBrightkite020201):
    K = 16
    checkins = '_'.join([SNAPBrightkite020201.checkins_super, SNAPBrightkite020201.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020201' + str(K)


class SNAPBrightkite02020117(SNAPBrightkite020201):
    K = 17
    checkins = '_'.join([SNAPBrightkite020201.checkins_super, SNAPBrightkite020201.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020201' + str(K)


class SNAPBrightkite02020118(SNAPBrightkite020201):
    K = 18
    checkins = '_'.join([SNAPBrightkite020201.checkins_super, SNAPBrightkite020201.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020201' + str(K)


class SNAPBrightkite02020119(SNAPBrightkite020201):
    K = 19
    checkins = '_'.join([SNAPBrightkite020201.checkins_super, SNAPBrightkite020201.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020201' + str(K)


class SNAPBrightkite02020120(SNAPBrightkite020201):
    K = 20
    checkins = '_'.join([SNAPBrightkite020201.checkins_super, SNAPBrightkite020201.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020201' + str(K)


class SNAPBrightkite020202(SNAPBrightkite0202):
    checkins_super = SNAPBrightkite0202.checkins.name
    k_anonymity_method = 'EnhancedCADSA'
    max_cached_time = 3600


class SNAPBrightkite02020203(SNAPBrightkite020202):
    K = 3
    checkins = '_'.join([SNAPBrightkite020202.checkins_super, SNAPBrightkite020202.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0202020' + str(K)


class SNAPBrightkite02020204(SNAPBrightkite020202):
    K = 4
    checkins = '_'.join([SNAPBrightkite020202.checkins_super, SNAPBrightkite020202.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0202020' + str(K)


class SNAPBrightkite02020205(SNAPBrightkite020202):
    K = 5
    checkins = '_'.join([SNAPBrightkite020202.checkins_super, SNAPBrightkite020202.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0202020' + str(K)


class SNAPBrightkite02020206(SNAPBrightkite020202):
    K = 6
    checkins = '_'.join([SNAPBrightkite020202.checkins_super, SNAPBrightkite020202.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0202020' + str(K)


class SNAPBrightkite02020207(SNAPBrightkite020202):
    K = 7
    checkins = '_'.join([SNAPBrightkite020202.checkins_super, SNAPBrightkite020202.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0202020' + str(K)


class SNAPBrightkite02020208(SNAPBrightkite020202):
    K = 8
    checkins = '_'.join([SNAPBrightkite020202.checkins_super, SNAPBrightkite020202.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0202020' + str(K)


class SNAPBrightkite02020209(SNAPBrightkite020202):
    K = 9
    checkins = '_'.join([SNAPBrightkite020202.checkins_super, SNAPBrightkite020202.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite0202020' + str(K)


class SNAPBrightkite02020210(SNAPBrightkite020202):
    K = 10
    checkins = '_'.join([SNAPBrightkite020202.checkins_super, SNAPBrightkite020202.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020202' + str(K)


class SNAPBrightkite02020211(SNAPBrightkite020202):
    K = 11
    checkins = '_'.join([SNAPBrightkite020202.checkins_super, SNAPBrightkite020202.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020202' + str(K)


class SNAPBrightkite02020212(SNAPBrightkite020202):
    K = 12
    checkins = '_'.join([SNAPBrightkite020202.checkins_super, SNAPBrightkite020202.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020202' + str(K)


class SNAPBrightkite02020213(SNAPBrightkite020202):
    K = 13
    checkins = '_'.join([SNAPBrightkite020202.checkins_super, SNAPBrightkite020202.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020202' + str(K)


class SNAPBrightkite02020214(SNAPBrightkite020202):
    K = 14
    checkins = '_'.join([SNAPBrightkite020202.checkins_super, SNAPBrightkite020202.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020202' + str(K)


class SNAPBrightkite02020215(SNAPBrightkite020202):
    K = 15
    checkins = '_'.join([SNAPBrightkite020202.checkins_super, SNAPBrightkite020202.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020202' + str(K)


class SNAPBrightkite02020216(SNAPBrightkite020202):
    K = 16
    checkins = '_'.join([SNAPBrightkite020202.checkins_super, SNAPBrightkite020202.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020202' + str(K)


class SNAPBrightkite02020217(SNAPBrightkite020202):
    K = 17
    checkins = '_'.join([SNAPBrightkite020202.checkins_super, SNAPBrightkite020202.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020202' + str(K)


class SNAPBrightkite02020218(SNAPBrightkite020202):
    K = 18
    checkins = '_'.join([SNAPBrightkite020202.checkins_super, SNAPBrightkite020202.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020202' + str(K)


class SNAPBrightkite02020219(SNAPBrightkite020202):
    K = 19
    checkins = '_'.join([SNAPBrightkite020202.checkins_super, SNAPBrightkite020202.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020202' + str(K)


class SNAPBrightkite02020220(SNAPBrightkite020202):
    K = 20
    checkins = '_'.join([SNAPBrightkite020202.checkins_super, SNAPBrightkite020202.k_anonymity_method, 'K' + str(K)])
    name = 'SNAPBrightkite020202' + str(K)


class Gowalla(Database):
    Base = declarative_base()
    edges = Table('edges',
                  Base.metadata,
                  Column('userid', Integer,
                         ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True,
                         index=True),
                  Column('friendid', Integer,
                         ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True,
                         index=True))

    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True, index=True)
        global_userid = Column(Integer, unique=True, index=True)

        bookmarked_spots_count = Column(Integer)
        challenge_pin_count = Column(Integer)
        checkin_num = Column(Integer)
        country_pin_count = Column(Integer)
        friends_count = Column(Integer)
        highlights_count = Column(Integer)
        items_count = Column(Integer)
        photos_count = Column(Integer)
        pins_count = Column(Integer)
        places_num = Column(Integer)
        province_pin_count = Column(Integer)
        region_pin_count = Column(Integer)
        stamps_count = Column(Integer)
        state_pin_count = Column(Integer)
        trips_count = Column(Integer)

        followers = relationship('User',
                                 secondary='edges',
                                 primaryjoin='User.id==edges.c.userid',
                                 secondaryjoin='User.id==edges.c.friendid',
                                 back_populates='followees',
                                 passive_deletes=True)
        followees = relationship('User',
                                 secondary='edges',
                                 primaryjoin='User.id==edges.c.friendid',
                                 secondaryjoin='User.id==edges.c.userid',
                                 back_populates='followers',
                                 passive_deletes=True)
        locations = relationship('Location',
                                 secondary='checkins',
                                 primaryjoin='User.id==checkins.c.userid',
                                 secondaryjoin='checkins.c.locid==Location.id',
                                 back_populates='visitors',
                                 passive_deletes=True)
        checkins = relationship('Checkin',
                                back_populates='user',
                                passive_deletes=True)

    class Location(Base):
        __tablename__ = 'locations'
        # __table_args__ = (UniqueConstraint('lon', 'lat', name='gps'),)

        id = Column(Integer, primary_key=True, index=True)
        lon = Column(REAL, index=True)
        lat = Column(REAL, index=True)

        name = Column(Text)
        city_state = Column(Text)
        created_at = Column(DateTime)
        photos_count = Column(Integer)
        checkins_count = Column(Integer)
        users_count = Column(Integer)
        radius_meters = Column(Integer)
        highlights_count = Column(Integer)
        items_count = Column(Integer)
        max_items_count = Column(Integer)
        spot_categories = Column(Text)

        visitors = relationship('User',
                                secondary='checkins',
                                primaryjoin='Location.id==checkins.c.locid',
                                secondaryjoin='User.id==checkins.c.userid',
                                back_populates='locations',
                                passive_deletes=True)
        checkins = relationship('Checkin',
                                back_populates='location',
                                passive_deletes=True)

    class Checkin(Base):
        __tablename__ = 'checkins'

        id = Column(Integer, primary_key=True, autoincrement=True)
        userid = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
        locdatetime = Column(DateTime, index=True)
        locid = Column(Integer, ForeignKey('locations.id', ondelete='CASCADE'), index=True)

        user = relationship('User',
                            back_populates='checkins',
                            passive_deletes=True)
        location = relationship('Location',
                                back_populates='checkins',
                                passive_deletes=True)

    checkins = Checkin.__table__
    csvs = {'gowalla_checkins': 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\gowalla_checkins.csv',
            'gowalla_edges': 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\gowalla_friendship.csv',
            'gowalla_userinfo': 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\gowalla_userinfo.csv',
            'gowalla_spots_subset1':
                'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\gowalla_spots_subset1.csv',
            'gowalla_spots_subset2':
                'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\gowalla_spots_subset2.csv'}
    datetime_range = [datetime(2009, 1, 21, 16, 40, 55), datetime(2011, 8, 16, 18, 54, 25)]  # all datetimes
    name = 'Gowalla'
    dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
    locations = Location.__table__
    locdatetime_format = '%Y-%m-%d %H:%M:%S'
    ranges = [-180.0, 180.0, -80.0, 80.0]
    url = 'sqlite:///' + dbfilepath
    users = User.__table__


class Gowalla0201(Gowalla):
    Base = declarative_base()
    edges = Table('edges',
                  Base.metadata,
                  Column('userid', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
                         primary_key=True, index=True),
                  Column('friendid', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
                         primary_key=True, index=True))

    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True, index=True)
        global_userid = Column(Integer, unique=True, index=True)

        bookmarked_spots_count = Column(Integer)
        challenge_pin_count = Column(Integer)
        checkin_num = Column(Integer)
        country_pin_count = Column(Integer)
        friends_count = Column(Integer)
        highlights_count = Column(Integer)
        items_count = Column(Integer)
        photos_count = Column(Integer)
        pins_count = Column(Integer)
        places_num = Column(Integer)
        province_pin_count = Column(Integer)
        region_pin_count = Column(Integer)
        stamps_count = Column(Integer)
        state_pin_count = Column(Integer)
        trips_count = Column(Integer)

        followers = relationship('User',
                                 secondary='edges',
                                 primaryjoin='User.id==edges.c.userid',
                                 secondaryjoin='User.id==edges.c.friendid',
                                 back_populates='followees',
                                 passive_deletes=True)
        followees = relationship('User',
                                 secondary='edges',
                                 primaryjoin='User.id==edges.c.friendid',
                                 secondaryjoin='User.id==edges.c.userid',
                                 back_populates='followers',
                                 passive_deletes=True)
        locations = relationship('Location',
                                 secondary='checkins',
                                 primaryjoin='User.id==checkins.c.userid',
                                 secondaryjoin='checkins.c.locid==Location.id',
                                 back_populates='visitors',
                                 passive_deletes=True)
        checkins = relationship('Checkin',
                                back_populates='user',
                                passive_deletes=True)

    class Location(Base):
        __tablename__ = 'locations'
        # __table_args__ = (UniqueConstraint('lon', 'lat', name='gps'),)

        id = Column(Integer, primary_key=True, index=True)

        name = Column(Text)
        city_state = Column(Text)
        created_at = Column(DateTime)
        photos_count = Column(Integer)
        checkins_count = Column(Integer)
        users_count = Column(Integer)
        radius_meters = Column(Integer)
        highlights_count = Column(Integer)
        items_count = Column(Integer)
        max_items_count = Column(Integer)
        spot_categories = Column(Text)

        visitors = relationship('User',
                                secondary='checkins',
                                primaryjoin='Location.id==checkins.c.locid',
                                secondaryjoin='User.id==checkins.c.userid',
                                back_populates='locations',
                                passive_deletes=True)
        checkins = relationship('Checkin',
                                back_populates='location',
                                passive_deletes=True)

    class Checkin(Base):
        __tablename__ = 'checkins'

        id = Column(Integer, primary_key=True)  # auto_increment=False
        userid = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
        locdatetime = Column(DateTime, index=True)
        lon = Column(REAL, index=True)
        lat = Column(REAL, index=True)
        locid = Column(Integer, ForeignKey('locations.id', ondelete='CASCADE'), index=True)
        gridlon = Column(Integer, index=True, nullable=True)  # new
        gridlat = Column(Integer, index=True, nullable=True)  # new
        gridid = Column(Integer, index=True, nullable=True)  # new
        clstlon = Column(REAL, index=True, nullable=True)  # new
        clstlat = Column(REAL, index=True, nullable=True)  # new
        clstid = Column(Integer, index=True, nullable=True)  # new

        user = relationship('User',
                            back_populates='checkins',
                            passive_deletes=True)
        location = relationship('Location',
                                back_populates='checkins',
                                passive_deletes=True)

    checkins = Checkin.__table__
    cluster_method = 'k-means'
    cluster_num = 100
    name = 'Gowalla0201'
    dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
    locations = Location.__table__
    min_tracelength = 20  # 1 means no filtering
    ranges = [-122.5153, -122.3789, 37.7084, 37.8130]  # San Francisco, 12km x 12km
    # ranges = [-122.5153, -122.3789, 37.5395, 37.7901]  # San Francisco in 'walk2friends'. 12km x 28km
    gridmap = GridMap(ranges=ranges, granularity=[0.005527, 0.004482])  # 500m x 500m
    subsample_rate = 1  # seconds, '1' or None means no subsampling.
    timezone_offset = -7  # local time = UTC - 7 hours
    url = 'sqlite:///' + dbfilepath
    users = User.__table__


class Gowalla020101(Gowalla0201):
    checkins_super = Gowalla0201.checkins.name
    k_anonymity_method = 'EnhancedDLS'


class Gowalla02010103(Gowalla020101):
    K = 3
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0201010' + str(K)


class Gowalla02010104(Gowalla020101):
    K = 4
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0201010' + str(K)


class Gowalla02010105(Gowalla020101):
    K = 5
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0201010' + str(K)


class Gowalla02010106(Gowalla020101):
    K = 6
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0201010' + str(K)


class Gowalla02010107(Gowalla020101):
    K = 7
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0201010' + str(K)


class Gowalla02010108(Gowalla020101):
    K = 8
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0201010' + str(K)


class Gowalla02010109(Gowalla020101):
    K = 9
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0201010' + str(K)


class Gowalla02010110(Gowalla020101):
    K = 10
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020101' + str(K)


class Gowalla02010111(Gowalla020101):
    K = 11
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020101' + str(K)


class Gowalla02010112(Gowalla020101):
    K = 12
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020101' + str(K)


class Gowalla02010113(Gowalla020101):
    K = 13
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020101' + str(K)


class Gowalla02010114(Gowalla020101):
    K = 14
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020101' + str(K)


class Gowalla02010115(Gowalla020101):
    K = 15
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020101' + str(K)


class Gowalla02010116(Gowalla020101):
    K = 16
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020101' + str(K)


class Gowalla02010117(Gowalla020101):
    K = 17
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020101' + str(K)


class Gowalla02010118(Gowalla020101):
    K = 18
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020101' + str(K)


class Gowalla02010119(Gowalla020101):
    K = 19
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020101' + str(K)


class Gowalla02010120(Gowalla020101):
    K = 20
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020101' + str(K)


class Gowalla020102(Gowalla0201):
    checkins_super = Gowalla0201.checkins.name
    k_anonymity_method = 'EnhancedCADSA'
    max_cached_time = 3600


class Gowalla02010203(Gowalla020102):
    K = 3
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0201020' + str(K)


class Gowalla02010204(Gowalla020102):
    K = 4
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0201020' + str(K)


class Gowalla02010205(Gowalla020102):
    K = 5
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0201020' + str(K)


class Gowalla02010206(Gowalla020102):
    K = 6
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0201020' + str(K)


class Gowalla02010207(Gowalla020102):
    K = 7
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0201020' + str(K)


class Gowalla02010208(Gowalla020102):
    K = 8
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0201020' + str(K)


class Gowalla02010209(Gowalla020102):
    K = 9
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0201020' + str(K)


class Gowalla02010210(Gowalla020102):
    K = 10
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020102' + str(K)


class Gowalla02010211(Gowalla020102):
    K = 11
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020102' + str(K)


class Gowalla02010212(Gowalla020102):
    K = 12
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020102' + str(K)


class Gowalla02010213(Gowalla020102):
    K = 13
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020102' + str(K)


class Gowalla02010214(Gowalla020102):
    K = 14
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020102' + str(K)


class Gowalla02010215(Gowalla020102):
    K = 15
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020102' + str(K)


class Gowalla02010216(Gowalla020102):
    K = 16
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020102' + str(K)


class Gowalla02010217(Gowalla020102):
    K = 17
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020102' + str(K)


class Gowalla02010218(Gowalla020102):
    K = 18
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020102' + str(K)


class Gowalla02010219(Gowalla020102):
    K = 19
    checkins = '_'.join([Gowalla020101.checkins_super, Gowalla020102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020102' + str(K)


class Gowalla02010220(Gowalla020102):
    K = 20
    checkins = '_'.join([Gowalla020102.checkins_super, Gowalla020102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020102' + str(K)


class Gowalla0202(Gowalla0201):
    cluster_num = 200
    name = 'Gowalla0202'
    dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
    url = 'sqlite:///' + dbfilepath


class Gowalla020201(Gowalla0202):
    checkins_super = Gowalla0202.checkins.name
    k_anonymity_method = 'EnhancedDLS'


class Gowalla02020103(Gowalla020201):
    K = 3
    checkins = '_'.join([Gowalla020201.checkins_super, Gowalla020201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0202010' + str(K)


class Gowalla02020104(Gowalla020201):
    K = 4
    checkins = '_'.join([Gowalla020201.checkins_super, Gowalla020201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0202010' + str(K)


class Gowalla02020105(Gowalla020201):
    K = 5
    checkins = '_'.join([Gowalla020201.checkins_super, Gowalla020201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0202010' + str(K)


class Gowalla02020106(Gowalla020201):
    K = 6
    checkins = '_'.join([Gowalla020201.checkins_super, Gowalla020201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0202010' + str(K)


class Gowalla02020107(Gowalla020201):
    K = 7
    checkins = '_'.join([Gowalla020201.checkins_super, Gowalla020201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0202010' + str(K)


class Gowalla02020108(Gowalla020201):
    K = 8
    checkins = '_'.join([Gowalla020201.checkins_super, Gowalla020201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0202010' + str(K)


class Gowalla02020109(Gowalla020201):
    K = 9
    checkins = '_'.join([Gowalla020201.checkins_super, Gowalla020201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0202010' + str(K)


class Gowalla02020110(Gowalla020201):
    K = 10
    checkins = '_'.join([Gowalla020201.checkins_super, Gowalla020201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020201' + str(K)


class Gowalla02020111(Gowalla020201):
    K = 11
    checkins = '_'.join([Gowalla020201.checkins_super, Gowalla020201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020201' + str(K)


class Gowalla02020112(Gowalla020201):
    K = 12
    checkins = '_'.join([Gowalla020201.checkins_super, Gowalla020201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020201' + str(K)


class Gowalla02020113(Gowalla020201):
    K = 13
    checkins = '_'.join([Gowalla020201.checkins_super, Gowalla020201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020201' + str(K)


class Gowalla02020114(Gowalla020201):
    K = 14
    checkins = '_'.join([Gowalla020201.checkins_super, Gowalla020201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020201' + str(K)


class Gowalla02020115(Gowalla020201):
    K = 15
    checkins = '_'.join([Gowalla020201.checkins_super, Gowalla020201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020201' + str(K)


class Gowalla02020116(Gowalla020201):
    K = 16
    checkins = '_'.join([Gowalla020201.checkins_super, Gowalla020201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020201' + str(K)


class Gowalla02020117(Gowalla020201):
    K = 17
    checkins = '_'.join([Gowalla020201.checkins_super, Gowalla020201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020201' + str(K)


class Gowalla020201118(Gowalla020201):
    K = 18
    checkins = '_'.join([Gowalla020201.checkins_super, Gowalla020201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020201' + str(K)


class Gowalla02020119(Gowalla020201):
    K = 19
    checkins = '_'.join([Gowalla020201.checkins_super, Gowalla020201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020201' + str(K)


class Gowalla02020120(Gowalla020201):
    K = 20
    checkins = '_'.join([Gowalla020201.checkins_super, Gowalla020201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020201' + str(K)


class Gowalla020202(Gowalla0202):
    checkins_super = Gowalla0202.checkins.name
    k_anonymity_method = 'EnhancedCADSA'
    max_cached_time = 3600


class Gowalla02020203(Gowalla020202):
    K = 3
    checkins = '_'.join([Gowalla020202.checkins_super, Gowalla020202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0202020' + str(K)


class Gowalla02020204(Gowalla020202):
    K = 4
    checkins = '_'.join([Gowalla020202.checkins_super, Gowalla020202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0202020' + str(K)


class Gowalla02020205(Gowalla020202):
    K = 5
    checkins = '_'.join([Gowalla020202.checkins_super, Gowalla020202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0202020' + str(K)


class Gowalla02020206(Gowalla020202):
    K = 6
    checkins = '_'.join([Gowalla020202.checkins_super, Gowalla020202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0202020' + str(K)


class Gowalla02020207(Gowalla020202):
    K = 7
    checkins = '_'.join([Gowalla020202.checkins_super, Gowalla020202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0202020' + str(K)


class Gowalla02020208(Gowalla020202):
    K = 8
    checkins = '_'.join([Gowalla020202.checkins_super, Gowalla020202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0202020' + str(K)


class Gowalla02020209(Gowalla020202):
    K = 9
    checkins = '_'.join([Gowalla020202.checkins_super, Gowalla020202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0202020' + str(K)


class Gowalla02020210(Gowalla020202):
    K = 10
    checkins = '_'.join([Gowalla020202.checkins_super, Gowalla020202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020202' + str(K)


class Gowalla02020211(Gowalla020202):
    K = 11
    checkins = '_'.join([Gowalla020202.checkins_super, Gowalla020202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020202' + str(K)


class Gowalla02020212(Gowalla020202):
    K = 12
    checkins = '_'.join([Gowalla020202.checkins_super, Gowalla020202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020202' + str(K)


class Gowalla020202113(Gowalla020202):
    K = 13
    checkins = '_'.join([Gowalla020202.checkins_super, Gowalla020202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020202' + str(K)


class Gowalla02020214(Gowalla020202):
    K = 14
    checkins = '_'.join([Gowalla020202.checkins_super, Gowalla020202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020202' + str(K)


class Gowalla02020215(Gowalla020202):
    K = 15
    checkins = '_'.join([Gowalla020202.checkins_super, Gowalla020202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020202' + str(K)


class Gowalla02020216(Gowalla020202):
    K = 16
    checkins = '_'.join([Gowalla020202.checkins_super, Gowalla020202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020202' + str(K)


class Gowalla02020217(Gowalla020202):
    K = 17
    checkins = '_'.join([Gowalla020202.checkins_super, Gowalla020202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020202' + str(K)


class Gowalla02020218(Gowalla020202):
    K = 18
    checkins = '_'.join([Gowalla020202.checkins_super, Gowalla020202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020202' + str(K)


class Gowalla02020219(Gowalla020202):
    K = 19
    checkins = '_'.join([Gowalla020202.checkins_super, Gowalla020202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020202' + str(K)


class Gowalla02020220(Gowalla020202):
    K = 20
    checkins = '_'.join([Gowalla020202.checkins_super, Gowalla020202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla020202' + str(K)


# class Gowalla0203(Gowalla0201):
#     cluster_num = 300
#     name = 'Gowalla0203'
#     dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
#     url = 'sqlite:///' + dbfilepath
#
#
# class Gowalla020301(Gowalla0203):
#     checkins_super = Gowalla0203.checkins.name
#     k_anonymity_method = 'EnhancedDLS'
#
#
# class Gowalla02030103(Gowalla020301):
#     K = 3
#     checkins = '_'.join([Gowalla020301.checkins_super, Gowalla020301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0203010' + str(K)
#
#
# class Gowalla02030105(Gowalla020301):
#     K = 5
#     checkins = '_'.join([Gowalla020301.checkins_super, Gowalla020301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0203010' + str(K)
#
#
# class Gowalla02030107(Gowalla020301):
#     K = 7
#     checkins = '_'.join([Gowalla020301.checkins_super, Gowalla020301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0203010' + str(K)
#
#
# class Gowalla02030110(Gowalla020301):
#     K = 10
#     checkins = '_'.join([Gowalla020301.checkins_super, Gowalla020301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla020301' + str(K)
#
#
# class Gowalla02030112(Gowalla020301):
#     K = 12
#     checkins = '_'.join([Gowalla020301.checkins_super, Gowalla020301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla020301' + str(K)
#
#
# class Gowalla02030115(Gowalla020301):
#     K = 15
#     checkins = '_'.join([Gowalla020301.checkins_super, Gowalla020301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla020301' + str(K)
#
#
# class Gowalla02030117(Gowalla020301):
#     K = 17
#     checkins = '_'.join([Gowalla020301.checkins_super, Gowalla020301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla020301' + str(K)
#
#
# class Gowalla02030120(Gowalla020301):
#     K = 20
#     checkins = '_'.join([Gowalla020301.checkins_super, Gowalla020301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla020301' + str(K)
#
#
# class Gowalla020302(Gowalla0203):
#     checkins_super = Gowalla0203.checkins.name
#     k_anonymity_method = 'EnhancedCADSA'
#     max_cached_time = 3600
#
#
# class Gowalla02030203(Gowalla020302):
#     K = 3
#     checkins = '_'.join([Gowalla020302.checkins_super, Gowalla020302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0203020' + str(K)
#
#
# class Gowalla02030205(Gowalla020302):
#     K = 5
#     checkins = '_'.join([Gowalla020302.checkins_super, Gowalla020302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0203020' + str(K)
#
#
# class Gowalla02030207(Gowalla020302):
#     K = 7
#     checkins = '_'.join([Gowalla020302.checkins_super, Gowalla020302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0203020' + str(K)
#
#
# class Gowalla02030210(Gowalla020302):
#     K = 10
#     checkins = '_'.join([Gowalla020302.checkins_super, Gowalla020302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla020302' + str(K)
#
#
# class Gowalla02030212(Gowalla020302):
#     K = 12
#     checkins = '_'.join([Gowalla020302.checkins_super, Gowalla020302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla020302' + str(K)
#
#
# class Gowalla02030215(Gowalla020302):
#     K = 15
#     checkins = '_'.join([Gowalla020302.checkins_super, Gowalla020302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla020302' + str(K)
#
#
# class Gowalla02030217(Gowalla020302):
#     K = 17
#     checkins = '_'.join([Gowalla020302.checkins_super, Gowalla020302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla020302' + str(K)
#
#
# class Gowalla02030220(Gowalla020302):
#     K = 20
#     checkins = '_'.join([Gowalla020302.checkins_super, Gowalla020302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla020302' + str(K)


class Gowalla0301(Gowalla):
    Base = declarative_base()
    edges = Table('edges',
                  Base.metadata,
                  Column('userid', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
                         primary_key=True, index=True),
                  Column('friendid', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
                         primary_key=True, index=True))

    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True, index=True)
        global_userid = Column(Integer, unique=True, index=True)

        followers = relationship('User',
                                 secondary='edges',
                                 primaryjoin='User.id==edges.c.userid',
                                 secondaryjoin='User.id==edges.c.friendid',
                                 back_populates='followees',
                                 passive_deletes=True)
        followees = relationship('User',
                                 secondary='edges',
                                 primaryjoin='User.id==edges.c.friendid',
                                 secondaryjoin='User.id==edges.c.userid',
                                 back_populates='followers',
                                 passive_deletes=True)
        locations = relationship('Location',
                                 secondary='checkins',
                                 primaryjoin='User.id==checkins.c.userid',
                                 secondaryjoin='checkins.c.locid==Location.id',
                                 back_populates='visitors',
                                 passive_deletes=True)
        checkins = relationship('Checkin',
                                back_populates='user',
                                passive_deletes=True)

    class Location(Base):
        __tablename__ = 'locations'
        # __table_args__ = (UniqueConstraint('lon', 'lat', name='gps'),)

        id = Column(Integer, primary_key=True, index=True)

        visitors = relationship('User',
                                secondary='checkins',
                                primaryjoin='Location.id==checkins.c.locid',
                                secondaryjoin='User.id==checkins.c.userid',
                                back_populates='locations',
                                passive_deletes=True)
        checkins = relationship('Checkin',
                                back_populates='location',
                                passive_deletes=True)

    class Checkin(Base):
        __tablename__ = 'checkins'

        id = Column(Integer, primary_key=True)  # auto_increment=False
        userid = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
        locdatetime = Column(DateTime, index=True)
        lon = Column(REAL, index=True)
        lat = Column(REAL, index=True)
        locid = Column(Integer, ForeignKey('locations.id', ondelete='CASCADE'), index=True)
        gridlon = Column(Integer, index=True, nullable=True)  # new
        gridlat = Column(Integer, index=True, nullable=True)  # new
        gridid = Column(Integer, index=True, nullable=True)  # new
        clstlon = Column(REAL, index=True, nullable=True)  # new
        clstlat = Column(REAL, index=True, nullable=True)  # new
        clstid = Column(Integer, index=True, nullable=True)  # new

        user = relationship('User',
                            back_populates='checkins',
                            passive_deletes=True)
        location = relationship('Location',
                                back_populates='checkins',
                                passive_deletes=True)

    checkins = Checkin.__table__
    cluster_method = 'k-means'
    cluster_num = 100
    name = 'Gowalla0301'
    dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
    locations = Location.__table__
    min_tracelength = 20  # 1 means no filtering
    ranges = [-74.020100, -73.934819, 40.699995, 40.813415]  # New York City, US  # 8km x 13km
    # ranges = [-74.052914, -73.875168, 40.656702, 40.836357]  # New York City, US  # 17km x 20km
    gridmap = GridMap(ranges=ranges, granularity=[0.005340, 0.004460])  # 500m x 500m
    subsample_rate = 1  # seconds, '1' or None means no subsampling
    timezone_offset = -4  # local time = UTC - 4 hours
    url = 'sqlite:///' + dbfilepath
    users = User.__table__


class Gowalla030101(Gowalla0301):
    checkins_super = Gowalla0301.checkins.name
    k_anonymity_method = 'EnhancedDLS'


class Gowalla03010103(Gowalla030101):
    K = 3
    checkins = '_'.join([Gowalla030101.checkins_super, Gowalla030101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0301010' + str(K)


class Gowalla03010104(Gowalla030101):
    K = 4
    checkins = '_'.join([Gowalla030101.checkins_super, Gowalla030101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0301010' + str(K)


class Gowalla03010105(Gowalla030101):
    K = 5
    checkins = '_'.join([Gowalla030101.checkins_super, Gowalla030101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0301010' + str(K)


class Gowalla03010106(Gowalla030101):
    K = 6
    checkins = '_'.join([Gowalla030101.checkins_super, Gowalla030101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0301010' + str(K)


class Gowalla03010107(Gowalla030101):
    K = 7
    checkins = '_'.join([Gowalla030101.checkins_super, Gowalla030101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0301010' + str(K)


class Gowalla03010108(Gowalla030101):
    K = 8
    checkins = '_'.join([Gowalla030101.checkins_super, Gowalla030101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0301010' + str(K)


class Gowalla03010109(Gowalla030101):
    K = 9
    checkins = '_'.join([Gowalla030101.checkins_super, Gowalla030101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0301010' + str(K)


class Gowalla03010110(Gowalla030101):
    K = 10
    checkins = '_'.join([Gowalla030101.checkins_super, Gowalla030101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030101' + str(K)


class Gowalla03010111(Gowalla030101):
    K = 11
    checkins = '_'.join([Gowalla030101.checkins_super, Gowalla030101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030101' + str(K)


class Gowalla03010112(Gowalla030101):
    K = 12
    checkins = '_'.join([Gowalla030101.checkins_super, Gowalla030101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030101' + str(K)


class Gowalla03010113(Gowalla030101):
    K = 13
    checkins = '_'.join([Gowalla030101.checkins_super, Gowalla030101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030101' + str(K)


class Gowalla03010114(Gowalla030101):
    K = 14
    checkins = '_'.join([Gowalla030101.checkins_super, Gowalla030101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030101' + str(K)


class Gowalla03010115(Gowalla030101):
    K = 15
    checkins = '_'.join([Gowalla030101.checkins_super, Gowalla030101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030101' + str(K)


class Gowalla03010116(Gowalla030101):
    K = 16
    checkins = '_'.join([Gowalla030101.checkins_super, Gowalla030101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030101' + str(K)


class Gowalla03010117(Gowalla030101):
    K = 17
    checkins = '_'.join([Gowalla030101.checkins_super, Gowalla030101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030101' + str(K)


class Gowalla03010118(Gowalla030101):
    K = 18
    checkins = '_'.join([Gowalla030101.checkins_super, Gowalla030101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030101' + str(K)


class Gowalla03010119(Gowalla030101):
    K = 19
    checkins = '_'.join([Gowalla030101.checkins_super, Gowalla030101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030101' + str(K)


class Gowalla03010120(Gowalla030101):
    K = 20
    checkins = '_'.join([Gowalla030101.checkins_super, Gowalla030101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030101' + str(K)


class Gowalla030102(Gowalla0301):
    checkins_super = Gowalla0301.checkins.name
    k_anonymity_method = 'EnhancedCADSA'
    max_cached_time = 3600


class Gowalla03010203(Gowalla030102):
    K = 3
    checkins = '_'.join([Gowalla030102.checkins_super, Gowalla030102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0301020' + str(K)


class Gowalla03010204(Gowalla030102):
    K = 4
    checkins = '_'.join([Gowalla030102.checkins_super, Gowalla030102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0301020' + str(K)


class Gowalla03010205(Gowalla030102):
    K = 5
    checkins = '_'.join([Gowalla030102.checkins_super, Gowalla030102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0301020' + str(K)


class Gowalla03010206(Gowalla030102):
    K = 6
    checkins = '_'.join([Gowalla030102.checkins_super, Gowalla030102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0301020' + str(K)


class Gowalla03010207(Gowalla030102):
    K = 7
    checkins = '_'.join([Gowalla030102.checkins_super, Gowalla030102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0301020' + str(K)


class Gowalla03010208(Gowalla030102):
    K = 8
    checkins = '_'.join([Gowalla030102.checkins_super, Gowalla030102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0301020' + str(K)


class Gowalla03010209(Gowalla030102):
    K = 9
    checkins = '_'.join([Gowalla030102.checkins_super, Gowalla030102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0301020' + str(K)


class Gowalla03010210(Gowalla030102):
    K = 10
    checkins = '_'.join([Gowalla030102.checkins_super, Gowalla030102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030102' + str(K)


class Gowalla03010211(Gowalla030102):
    K = 11
    checkins = '_'.join([Gowalla030102.checkins_super, Gowalla030102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030102' + str(K)


class Gowalla03010212(Gowalla030102):
    K = 12
    checkins = '_'.join([Gowalla030102.checkins_super, Gowalla030102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030102' + str(K)


class Gowalla03010213(Gowalla030102):
    K = 13
    checkins = '_'.join([Gowalla030102.checkins_super, Gowalla030102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030102' + str(K)


class Gowalla03010214(Gowalla030102):
    K = 14
    checkins = '_'.join([Gowalla030102.checkins_super, Gowalla030102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030102' + str(K)


class Gowalla03010215(Gowalla030102):
    K = 15
    checkins = '_'.join([Gowalla030102.checkins_super, Gowalla030102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030102' + str(K)


class Gowalla03010216(Gowalla030102):
    K = 16
    checkins = '_'.join([Gowalla030102.checkins_super, Gowalla030102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030102' + str(K)


class Gowalla03010217(Gowalla030102):
    K = 17
    checkins = '_'.join([Gowalla030102.checkins_super, Gowalla030102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030102' + str(K)


class Gowalla03010218(Gowalla030102):
    K = 18
    checkins = '_'.join([Gowalla030102.checkins_super, Gowalla030102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030102' + str(K)


class Gowalla03010219(Gowalla030102):
    K = 19
    checkins = '_'.join([Gowalla030102.checkins_super, Gowalla030102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030102' + str(K)


class Gowalla03010220(Gowalla030102):
    K = 20
    checkins = '_'.join([Gowalla030102.checkins_super, Gowalla030102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030102' + str(K)


class Gowalla0302(Gowalla0301):
    cluster_num = 200
    name = 'Gowalla0302'
    dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
    url = 'sqlite:///' + dbfilepath


class Gowalla030201(Gowalla0302):
    checkins_super = Gowalla0302.checkins.name
    k_anonymity_method = 'EnhancedDLS'


class Gowalla03020103(Gowalla030201):
    K = 3
    checkins = '_'.join([Gowalla030201.checkins_super, Gowalla030201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0302010' + str(K)


class Gowalla03020105(Gowalla030201):
    K = 5
    checkins = '_'.join([Gowalla030201.checkins_super, Gowalla030201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0302010' + str(K)


class Gowalla03020107(Gowalla030201):
    K = 7
    checkins = '_'.join([Gowalla030201.checkins_super, Gowalla030201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0302010' + str(K)


class Gowalla03020110(Gowalla030201):
    K = 10
    checkins = '_'.join([Gowalla030201.checkins_super, Gowalla030201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030201' + str(K)


class Gowalla03020112(Gowalla030201):
    K = 12
    checkins = '_'.join([Gowalla030201.checkins_super, Gowalla030201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030201' + str(K)


class Gowalla03020115(Gowalla030201):
    K = 15
    checkins = '_'.join([Gowalla030201.checkins_super, Gowalla030201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030201' + str(K)


class Gowalla03020117(Gowalla030201):
    K = 17
    checkins = '_'.join([Gowalla030201.checkins_super, Gowalla030201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030201' + str(K)


class Gowalla03020120(Gowalla030201):
    K = 20
    checkins = '_'.join([Gowalla030201.checkins_super, Gowalla030201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030201' + str(K)


class Gowalla030202(Gowalla0302):
    checkins_super = Gowalla0302.checkins.name
    k_anonymity_method = 'EnhancedCADSA'
    max_cached_time = 3600


class Gowalla03020203(Gowalla030202):
    K = 3
    checkins = '_'.join([Gowalla030202.checkins_super, Gowalla030202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0302020' + str(K)


class Gowalla03020205(Gowalla030202):
    K = 5
    checkins = '_'.join([Gowalla030202.checkins_super, Gowalla030202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0302020' + str(K)


class Gowalla03020207(Gowalla030202):
    K = 7
    checkins = '_'.join([Gowalla030202.checkins_super, Gowalla030202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0302020' + str(K)


class Gowalla03020210(Gowalla030202):
    K = 10
    checkins = '_'.join([Gowalla030202.checkins_super, Gowalla030202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030202' + str(K)


class Gowalla03020212(Gowalla030202):
    K = 12
    checkins = '_'.join([Gowalla030202.checkins_super, Gowalla030202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030202' + str(K)


class Gowalla03020215(Gowalla030202):
    K = 15
    checkins = '_'.join([Gowalla030202.checkins_super, Gowalla030202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030202' + str(K)


class Gowalla03020217(Gowalla030202):
    K = 17
    checkins = '_'.join([Gowalla030202.checkins_super, Gowalla030202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030202' + str(K)


class Gowalla03020220(Gowalla030202):
    K = 20
    checkins = '_'.join([Gowalla030202.checkins_super, Gowalla030202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla030202' + str(K)


# class Gowalla0303(Gowalla0301):
#     cluster_num = 300
#     name = 'Gowalla0303'
#     dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
#     url = 'sqlite:///' + dbfilepath
#
#
# class Gowalla030301(Gowalla0303):
#     checkins_super = Gowalla0303.checkins.name
#     k_anonymity_method = 'EnhancedDLS'
#
#
# class Gowalla03030103(Gowalla030301):
#     K = 3
#     checkins = '_'.join([Gowalla030301.checkins_super, Gowalla030301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0303010' + str(K)
#
#
# class Gowalla03030105(Gowalla030301):
#     K = 5
#     checkins = '_'.join([Gowalla030301.checkins_super, Gowalla030301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0303010' + str(K)
#
#
# class Gowalla03030107(Gowalla030301):
#     K = 7
#     checkins = '_'.join([Gowalla030301.checkins_super, Gowalla030301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0303010' + str(K)
#
#
# class Gowalla03030110(Gowalla030301):
#     K = 10
#     checkins = '_'.join([Gowalla030301.checkins_super, Gowalla030301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla030301' + str(K)
#
#
# class Gowalla03030112(Gowalla030301):
#     K = 12
#     checkins = '_'.join([Gowalla030301.checkins_super, Gowalla030301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla030301' + str(K)
#
#
# class Gowalla03030115(Gowalla030301):
#     K = 15
#     checkins = '_'.join([Gowalla030301.checkins_super, Gowalla030301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla030301' + str(K)
#
#
# class Gowalla03030117(Gowalla030301):
#     K = 17
#     checkins = '_'.join([Gowalla030301.checkins_super, Gowalla030301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla030301' + str(K)
#
#
# class Gowalla03030120(Gowalla030301):
#     K = 20
#     checkins = '_'.join([Gowalla030301.checkins_super, Gowalla030301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla030301' + str(K)
#
#
# class Gowalla030302(Gowalla0303):
#     checkins_super = Gowalla0303.checkins.name
#     k_anonymity_method = 'EnhancedCADSA'
#     max_cached_time = 3600
#
#
# class Gowalla03030203(Gowalla030302):
#     K = 3
#     checkins = '_'.join([Gowalla030302.checkins_super, Gowalla030302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0303020' + str(K)
#
#
# class Gowalla03030205(Gowalla030302):
#     K = 5
#     checkins = '_'.join([Gowalla030302.checkins_super, Gowalla030302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0303020' + str(K)
#
#
# class Gowalla03030207(Gowalla030302):
#     K = 7
#     checkins = '_'.join([Gowalla030302.checkins_super, Gowalla030302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0303020' + str(K)
#
#
# class Gowalla03030210(Gowalla030302):
#     K = 10
#     checkins = '_'.join([Gowalla030302.checkins_super, Gowalla030302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla030302' + str(K)
#
#
# class Gowalla03030212(Gowalla030302):
#     K = 12
#     checkins = '_'.join([Gowalla030302.checkins_super, Gowalla030302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla030302' + str(K)
#
#
# class Gowalla03030215(Gowalla030302):
#     K = 15
#     checkins = '_'.join([Gowalla030302.checkins_super, Gowalla030302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla030302' + str(K)
#
#
# class Gowalla03030217(Gowalla030302):
#     K = 17
#     checkins = '_'.join([Gowalla030302.checkins_super, Gowalla030302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla030302' + str(K)
#
#
# class Gowalla03030220(Gowalla030302):
#     K = 20
#     checkins = '_'.join([Gowalla030302.checkins_super, Gowalla030302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla030302' + str(K)


class Gowalla0401(Gowalla):
    Base = declarative_base()
    edges = Table('edges',
                  Base.metadata,
                  Column('userid', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
                         primary_key=True, index=True),
                  Column('friendid', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
                         primary_key=True, index=True))

    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True, index=True)
        global_userid = Column(Integer, unique=True, index=True)

        followers = relationship('User',
                                 secondary='edges',
                                 primaryjoin='User.id==edges.c.userid',
                                 secondaryjoin='User.id==edges.c.friendid',
                                 back_populates='followees',
                                 passive_deletes=True)
        followees = relationship('User',
                                 secondary='edges',
                                 primaryjoin='User.id==edges.c.friendid',
                                 secondaryjoin='User.id==edges.c.userid',
                                 back_populates='followers',
                                 passive_deletes=True)
        locations = relationship('Location',
                                 secondary='checkins',
                                 primaryjoin='User.id==checkins.c.userid',
                                 secondaryjoin='checkins.c.locid==Location.id',
                                 back_populates='visitors',
                                 passive_deletes=True)
        checkins = relationship('Checkin',
                                back_populates='user',
                                passive_deletes=True)

    class Location(Base):
        __tablename__ = 'locations'
        # __table_args__ = (UniqueConstraint('lon', 'lat', name='gps'),)

        id = Column(Integer, primary_key=True, index=True)

        visitors = relationship('User',
                                secondary='checkins',
                                primaryjoin='Location.id==checkins.c.locid',
                                secondaryjoin='User.id==checkins.c.userid',
                                back_populates='locations',
                                passive_deletes=True)
        checkins = relationship('Checkin',
                                back_populates='location',
                                passive_deletes=True)

    class Checkin(Base):
        __tablename__ = 'checkins'

        id = Column(Integer, primary_key=True)  # auto_increment=False
        userid = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
        locdatetime = Column(DateTime, index=True)
        lon = Column(REAL, index=True)
        lat = Column(REAL, index=True)
        locid = Column(Integer, ForeignKey('locations.id', ondelete='CASCADE'), index=True)
        gridlon = Column(Integer, index=True, nullable=True)  # new
        gridlat = Column(Integer, index=True, nullable=True)  # new
        gridid = Column(Integer, index=True, nullable=True)  # new
        clstlon = Column(REAL, index=True, nullable=True)  # new
        clstlat = Column(REAL, index=True, nullable=True)  # new
        clstid = Column(Integer, index=True, nullable=True)  # new

        user = relationship('User',
                            back_populates='checkins',
                            passive_deletes=True)
        location = relationship('Location',
                                back_populates='checkins',
                                passive_deletes=True)

    checkins = Checkin.__table__
    cluster_method = 'k-means'
    cluster_num = 100
    name = 'Gowalla0401'
    dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
    locations = Location.__table__
    min_tracelength = 50  # 1 means no filtering, 50 will keep more friends than 20!
    ranges = [-97.812884, -97.691613, 30.234639, 30.334892]  # Austin, US  # 15km x 14km
    gridmap = GridMap(ranges=ranges, granularity=[0.0041615, 0.003617])  # 500m x 500m
    subsample_rate = 1  # seconds, '1' or None means no subsampling
    timezone_offset = -5  # local time = UTC - 5 hours
    url = 'sqlite:///' + dbfilepath
    users = User.__table__


class Gowalla040101(Gowalla0401):
    checkins_super = Gowalla0401.checkins.name
    k_anonymity_method = 'EnhancedDLS'


class Gowalla04010103(Gowalla040101):
    K = 3
    checkins = '_'.join([Gowalla040101.checkins_super, Gowalla040101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0401010' + str(K)


class Gowalla04010104(Gowalla040101):
    K = 4
    checkins = '_'.join([Gowalla040101.checkins_super, Gowalla040101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0401010' + str(K)


class Gowalla04010105(Gowalla040101):
    K = 5
    checkins = '_'.join([Gowalla040101.checkins_super, Gowalla040101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0401010' + str(K)


class Gowalla04010106(Gowalla040101):
    K = 6
    checkins = '_'.join([Gowalla040101.checkins_super, Gowalla040101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0401010' + str(K)


class Gowalla04010107(Gowalla040101):
    K = 7
    checkins = '_'.join([Gowalla040101.checkins_super, Gowalla040101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0401010' + str(K)


class Gowalla04010108(Gowalla040101):
    K = 8
    checkins = '_'.join([Gowalla040101.checkins_super, Gowalla040101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0401010' + str(K)


class Gowalla04010109(Gowalla040101):
    K = 9
    checkins = '_'.join([Gowalla040101.checkins_super, Gowalla040101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0401010' + str(K)


class Gowalla04010110(Gowalla040101):
    K = 10
    checkins = '_'.join([Gowalla040101.checkins_super, Gowalla040101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040101' + str(K)


class Gowalla04010111(Gowalla040101):
    K = 11
    checkins = '_'.join([Gowalla040101.checkins_super, Gowalla040101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040101' + str(K)


class Gowalla04010112(Gowalla040101):
    K = 12
    checkins = '_'.join([Gowalla040101.checkins_super, Gowalla040101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040101' + str(K)


class Gowalla04010113(Gowalla040101):
    K = 13
    checkins = '_'.join([Gowalla040101.checkins_super, Gowalla040101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040101' + str(K)


class Gowalla04010114(Gowalla040101):
    K = 14
    checkins = '_'.join([Gowalla040101.checkins_super, Gowalla040101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040101' + str(K)


class Gowalla04010115(Gowalla040101):
    K = 15
    checkins = '_'.join([Gowalla040101.checkins_super, Gowalla040101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040101' + str(K)


class Gowalla04010116(Gowalla040101):
    K = 16
    checkins = '_'.join([Gowalla040101.checkins_super, Gowalla040101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040101' + str(K)


class Gowalla04010117(Gowalla040101):
    K = 17
    checkins = '_'.join([Gowalla040101.checkins_super, Gowalla040101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040101' + str(K)


class Gowalla04010118(Gowalla040101):
    K = 18
    checkins = '_'.join([Gowalla040101.checkins_super, Gowalla040101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040101' + str(K)


class Gowalla04010119(Gowalla040101):
    K = 19
    checkins = '_'.join([Gowalla040101.checkins_super, Gowalla040101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040101' + str(K)


class Gowalla04010120(Gowalla040101):
    K = 20
    checkins = '_'.join([Gowalla040101.checkins_super, Gowalla040101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040101' + str(K)


class Gowalla040102(Gowalla0401):
    checkins_super = Gowalla0401.checkins.name
    k_anonymity_method = 'EnhancedCADSA'
    max_cached_time = 3600


class Gowalla04010203(Gowalla040102):
    K = 3
    checkins = '_'.join([Gowalla040102.checkins_super, Gowalla040102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0401020' + str(K)


class Gowalla04010204(Gowalla040102):
    K = 4
    checkins = '_'.join([Gowalla040102.checkins_super, Gowalla040102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0401020' + str(K)


class Gowalla04010205(Gowalla040102):
    K = 5
    checkins = '_'.join([Gowalla040102.checkins_super, Gowalla040102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0401020' + str(K)


class Gowalla04010206(Gowalla040102):
    K = 6
    checkins = '_'.join([Gowalla040102.checkins_super, Gowalla040102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0401020' + str(K)


class Gowalla04010207(Gowalla040102):
    K = 7
    checkins = '_'.join([Gowalla040102.checkins_super, Gowalla040102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0401020' + str(K)


class Gowalla04010208(Gowalla040102):
    K = 8
    checkins = '_'.join([Gowalla040102.checkins_super, Gowalla040102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0401020' + str(K)


class Gowalla04010209(Gowalla040102):
    K = 9
    checkins = '_'.join([Gowalla040102.checkins_super, Gowalla040102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0401020' + str(K)


class Gowalla04010210(Gowalla040102):
    K = 10
    checkins = '_'.join([Gowalla040102.checkins_super, Gowalla040102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040102' + str(K)


class Gowalla04010211(Gowalla040102):
    K = 11
    checkins = '_'.join([Gowalla040102.checkins_super, Gowalla040102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040102' + str(K)


class Gowalla04010212(Gowalla040102):
    K = 12
    checkins = '_'.join([Gowalla040102.checkins_super, Gowalla040102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040102' + str(K)


class Gowalla04010213(Gowalla040102):
    K = 13
    checkins = '_'.join([Gowalla040102.checkins_super, Gowalla040102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040102' + str(K)


class Gowalla04010214(Gowalla040102):
    K = 14
    checkins = '_'.join([Gowalla040102.checkins_super, Gowalla040102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040102' + str(K)


class Gowalla04010215(Gowalla040102):
    K = 15
    checkins = '_'.join([Gowalla040102.checkins_super, Gowalla040102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040102' + str(K)


class Gowalla04010216(Gowalla040102):
    K = 16
    checkins = '_'.join([Gowalla040102.checkins_super, Gowalla040102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040102' + str(K)


class Gowalla04010217(Gowalla040102):
    K = 17
    checkins = '_'.join([Gowalla040102.checkins_super, Gowalla040102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040102' + str(K)


class Gowalla04010218(Gowalla040102):
    K = 18
    checkins = '_'.join([Gowalla040102.checkins_super, Gowalla040102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040102' + str(K)


class Gowalla04010219(Gowalla040102):
    K = 19
    checkins = '_'.join([Gowalla040102.checkins_super, Gowalla040102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040102' + str(K)


class Gowalla04010220(Gowalla040102):
    K = 20
    checkins = '_'.join([Gowalla040102.checkins_super, Gowalla040102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040102' + str(K)


class Gowalla0402(Gowalla0401):
    cluster_num = 200
    name = 'Gowalla0402'
    dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
    url = 'sqlite:///' + dbfilepath


class Gowalla040201(Gowalla0402):
    checkins_super = Gowalla0402.checkins.name
    k_anonymity_method = 'EnhancedDLS'


class Gowalla04020103(Gowalla040201):
    K = 3
    checkins = '_'.join([Gowalla040201.checkins_super, Gowalla040201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0402010' + str(K)


class Gowalla04020105(Gowalla040201):
    K = 5
    checkins = '_'.join([Gowalla040201.checkins_super, Gowalla040201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0402010' + str(K)


class Gowalla04020107(Gowalla040201):
    K = 7
    checkins = '_'.join([Gowalla040201.checkins_super, Gowalla040201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0402010' + str(K)


class Gowalla04020110(Gowalla040201):
    K = 10
    checkins = '_'.join([Gowalla040201.checkins_super, Gowalla040201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040201' + str(K)


class Gowalla04020112(Gowalla040201):
    K = 12
    checkins = '_'.join([Gowalla040201.checkins_super, Gowalla040201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040201' + str(K)


class Gowalla04020115(Gowalla040201):
    K = 15
    checkins = '_'.join([Gowalla040201.checkins_super, Gowalla040201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040201' + str(K)


class Gowalla04020117(Gowalla040201):
    K = 17
    checkins = '_'.join([Gowalla040201.checkins_super, Gowalla040201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040201' + str(K)


class Gowalla04020120(Gowalla040201):
    K = 20
    checkins = '_'.join([Gowalla040201.checkins_super, Gowalla040201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040201' + str(K)


class Gowalla040202(Gowalla0402):
    checkins_super = Gowalla0402.checkins.name
    k_anonymity_method = 'EnhancedCADSA'
    max_cached_time = 3600


class Gowalla04020203(Gowalla040202):
    K = 3
    checkins = '_'.join([Gowalla040202.checkins_super, Gowalla040202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0402020' + str(K)


class Gowalla04020205(Gowalla040202):
    K = 5
    checkins = '_'.join([Gowalla040202.checkins_super, Gowalla040202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0402020' + str(K)


class Gowalla04020207(Gowalla040202):
    K = 7
    checkins = '_'.join([Gowalla040202.checkins_super, Gowalla040202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0402020' + str(K)


class Gowalla04020210(Gowalla040202):
    K = 10
    checkins = '_'.join([Gowalla040202.checkins_super, Gowalla040202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040202' + str(K)


class Gowalla04020212(Gowalla040202):
    K = 12
    checkins = '_'.join([Gowalla040202.checkins_super, Gowalla040202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040202' + str(K)


class Gowalla04020215(Gowalla040202):
    K = 15
    checkins = '_'.join([Gowalla040202.checkins_super, Gowalla040202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040202' + str(K)


class Gowalla04020217(Gowalla040202):
    K = 17
    checkins = '_'.join([Gowalla040202.checkins_super, Gowalla040202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040202' + str(K)


class Gowalla04020220(Gowalla040202):
    K = 20
    checkins = '_'.join([Gowalla040202.checkins_super, Gowalla040202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla040202' + str(K)


# class Gowalla0403(Gowalla0401):
#     cluster_num = 300
#     name = 'Gowalla0403'
#     dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
#     url = 'sqlite:///' + dbfilepath
#
#
# class Gowalla040301(Gowalla0403):
#     checkins_super = Gowalla0403.checkins.name
#     k_anonymity_method = 'EnhancedDLS'
#
#
# class Gowalla04030103(Gowalla040301):
#     K = 3
#     checkins = '_'.join([Gowalla040301.checkins_super, Gowalla040301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0403010' + str(K)
#
#
# class Gowalla04030105(Gowalla040301):
#     K = 5
#     checkins = '_'.join([Gowalla040301.checkins_super, Gowalla040301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0403010' + str(K)
#
#
# class Gowalla04030107(Gowalla040301):
#     K = 7
#     checkins = '_'.join([Gowalla040301.checkins_super, Gowalla040301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0403010' + str(K)
#
#
# class Gowalla04030110(Gowalla040301):
#     K = 10
#     checkins = '_'.join([Gowalla040301.checkins_super, Gowalla040301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla040301' + str(K)
#
#
# class Gowalla04030112(Gowalla040301):
#     K = 12
#     checkins = '_'.join([Gowalla040301.checkins_super, Gowalla040301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla040301' + str(K)
#
#
# class Gowalla04030115(Gowalla040301):
#     K = 15
#     checkins = '_'.join([Gowalla040301.checkins_super, Gowalla040301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla040301' + str(K)
#
#
# class Gowalla04030117(Gowalla040301):
#     K = 17
#     checkins = '_'.join([Gowalla040301.checkins_super, Gowalla040301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla040301' + str(K)
#
#
# class Gowalla04030120(Gowalla040301):
#     K = 20
#     checkins = '_'.join([Gowalla040301.checkins_super, Gowalla040301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla040301' + str(K)
#
#
# class Gowalla040302(Gowalla0403):
#     checkins_super = Gowalla0403.checkins.name
#     k_anonymity_method = 'EnhancedCADSA'
#     max_cached_time = 3600
#
#
# class Gowalla04030203(Gowalla040302):
#     K = 3
#     checkins = '_'.join([Gowalla040302.checkins_super, Gowalla040302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0403020' + str(K)
#
#
# class Gowalla04030205(Gowalla040302):
#     K = 5
#     checkins = '_'.join([Gowalla040302.checkins_super, Gowalla040302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0403020' + str(K)
#
#
# class Gowalla04030207(Gowalla040302):
#     K = 7
#     checkins = '_'.join([Gowalla040302.checkins_super, Gowalla040302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0403020' + str(K)
#
#
# class Gowalla04030210(Gowalla040302):
#     K = 10
#     checkins = '_'.join([Gowalla040302.checkins_super, Gowalla040302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla040302' + str(K)
#
#
# class Gowalla040302112(Gowalla040302):
#     K = 12
#     checkins = '_'.join([Gowalla040302.checkins_super, Gowalla040302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla040302' + str(K)
#
#
# class Gowalla04030215(Gowalla040302):
#     K = 15
#     checkins = '_'.join([Gowalla040302.checkins_super, Gowalla040302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla040302' + str(K)
#
#
# class Gowalla04030217(Gowalla040302):
#     K = 17
#     checkins = '_'.join([Gowalla040302.checkins_super, Gowalla040302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla040302' + str(K)
#
#
# class Gowalla04030220(Gowalla040302):
#     K = 20
#     checkins = '_'.join([Gowalla040302.checkins_super, Gowalla040302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla040302' + str(K)


class Gowalla0501(Gowalla):
    Base = declarative_base()
    edges = Table('edges',
                  Base.metadata,
                  Column('userid', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
                         primary_key=True, index=True),
                  Column('friendid', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
                         primary_key=True, index=True))

    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True, index=True)
        global_userid = Column(Integer, unique=True, index=True)

        followers = relationship('User',
                                 secondary='edges',
                                 primaryjoin='User.id==edges.c.userid',
                                 secondaryjoin='User.id==edges.c.friendid',
                                 back_populates='followees',
                                 passive_deletes=True)
        followees = relationship('User',
                                 secondary='edges',
                                 primaryjoin='User.id==edges.c.friendid',
                                 secondaryjoin='User.id==edges.c.userid',
                                 back_populates='followers',
                                 passive_deletes=True)
        locations = relationship('Location',
                                 secondary='checkins',
                                 primaryjoin='User.id==checkins.c.userid',
                                 secondaryjoin='checkins.c.locid==Location.id',
                                 back_populates='visitors',
                                 passive_deletes=True)
        checkins = relationship('Checkin',
                                back_populates='user',
                                passive_deletes=True)

    class Location(Base):
        __tablename__ = 'locations'
        # __table_args__ = (UniqueConstraint('lon', 'lat', name='gps'),)

        id = Column(Integer, primary_key=True, index=True)

        visitors = relationship('User',
                                secondary='checkins',
                                primaryjoin='Location.id==checkins.c.locid',
                                secondaryjoin='User.id==checkins.c.userid',
                                back_populates='locations',
                                passive_deletes=True)
        checkins = relationship('Checkin',
                                back_populates='location',
                                passive_deletes=True)

    class Checkin(Base):
        __tablename__ = 'checkins'

        id = Column(Integer, primary_key=True)  # auto_increment=False
        userid = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
        locdatetime = Column(DateTime, index=True)
        lon = Column(REAL, index=True)
        lat = Column(REAL, index=True)
        locid = Column(Integer, ForeignKey('locations.id', ondelete='CASCADE'), index=True)
        gridlon = Column(Integer, index=True, nullable=True)  # new
        gridlat = Column(Integer, index=True, nullable=True)  # new
        gridid = Column(Integer, index=True, nullable=True)  # new
        clstlon = Column(REAL, index=True, nullable=True)  # new
        clstlat = Column(REAL, index=True, nullable=True)  # new
        clstid = Column(Integer, index=True, nullable=True)  # new

        user = relationship('User',
                            back_populates='checkins',
                            passive_deletes=True)
        location = relationship('Location',
                                back_populates='checkins',
                                passive_deletes=True)

    checkins = Checkin.__table__
    cluster_method = 'k-means'
    cluster_num = 100
    name = 'Gowalla0501'
    dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
    locations = Location.__table__
    min_tracelength = 50  # 1 means no filtering
    ranges = [17.934368, 18.149311, 59.250076, 59.379162]  # Stockholm, SE  # 12km x 14km
    gridmap = GridMap(ranges=ranges, granularity=[0.0088272, 0.0045266])  # 500m x 500m
    subsample_rate = 1  # seconds, '1' or None means no subsampling
    timezone_offset = 2  # local time = UTC + 5 hours
    url = 'sqlite:///' + dbfilepath
    users = User.__table__


class Gowalla050101(Gowalla0501):
    checkins_super = Gowalla0501.checkins.name
    k_anonymity_method = 'EnhancedDLS'


class Gowalla05010103(Gowalla050101):
    K = 3
    checkins = '_'.join([Gowalla050101.checkins_super, Gowalla050101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0501010' + str(K)


class Gowalla05010105(Gowalla050101):
    K = 5
    checkins = '_'.join([Gowalla050101.checkins_super, Gowalla050101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0501010' + str(K)


class Gowalla05010107(Gowalla050101):
    K = 7
    checkins = '_'.join([Gowalla050101.checkins_super, Gowalla050101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0501010' + str(K)


class Gowalla05010110(Gowalla050101):
    K = 10
    checkins = '_'.join([Gowalla050101.checkins_super, Gowalla050101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050101' + str(K)


class Gowalla05010112(Gowalla050101):
    K = 12
    checkins = '_'.join([Gowalla050101.checkins_super, Gowalla050101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050101' + str(K)


class Gowalla05010115(Gowalla050101):
    K = 15
    checkins = '_'.join([Gowalla050101.checkins_super, Gowalla050101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050101' + str(K)


class Gowalla05010117(Gowalla050101):
    K = 17
    checkins = '_'.join([Gowalla050101.checkins_super, Gowalla050101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050101' + str(K)


class Gowalla05010120(Gowalla050101):
    K = 20
    checkins = '_'.join([Gowalla050101.checkins_super, Gowalla050101.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050101' + str(K)


class Gowalla050102(Gowalla0501):
    checkins_super = Gowalla0501.checkins.name
    k_anonymity_method = 'EnhancedCADSA'
    max_cached_time = 3600


class Gowalla05010203(Gowalla050102):
    K = 3
    checkins = '_'.join([Gowalla050102.checkins_super, Gowalla050102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0501020' + str(K)


class Gowalla05010205(Gowalla050102):
    K = 5
    checkins = '_'.join([Gowalla050102.checkins_super, Gowalla050102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0501020' + str(K)


class Gowalla05010207(Gowalla050102):
    K = 7
    checkins = '_'.join([Gowalla050102.checkins_super, Gowalla050102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0501020' + str(K)


class Gowalla05010210(Gowalla050102):
    K = 10
    checkins = '_'.join([Gowalla050102.checkins_super, Gowalla050102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050102' + str(K)


class Gowalla05010212(Gowalla050102):
    K = 12
    checkins = '_'.join([Gowalla050102.checkins_super, Gowalla050102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050102' + str(K)


class Gowalla05010215(Gowalla050102):
    K = 15
    checkins = '_'.join([Gowalla050102.checkins_super, Gowalla050102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050102' + str(K)


class Gowalla05010217(Gowalla050102):
    K = 17
    checkins = '_'.join([Gowalla050102.checkins_super, Gowalla050102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050102' + str(K)


class Gowalla05010220(Gowalla050102):
    K = 20
    checkins = '_'.join([Gowalla050102.checkins_super, Gowalla050102.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050102' + str(K)


class Gowalla0502(Gowalla0501):
    cluster_num = 200
    name = 'Gowalla0502'
    dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
    url = 'sqlite:///' + dbfilepath


class Gowalla050201(Gowalla0502):
    checkins_super = Gowalla0502.checkins.name
    k_anonymity_method = 'EnhancedDLS'


class Gowalla05020103(Gowalla050201):
    K = 3
    checkins = '_'.join([Gowalla050201.checkins_super, Gowalla050201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0502010' + str(K)


class Gowalla05020105(Gowalla050201):
    K = 5
    checkins = '_'.join([Gowalla050201.checkins_super, Gowalla050201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0502010' + str(K)


class Gowalla05020107(Gowalla050201):
    K = 7
    checkins = '_'.join([Gowalla050201.checkins_super, Gowalla050201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0502010' + str(K)


class Gowalla05020110(Gowalla050201):
    K = 10
    checkins = '_'.join([Gowalla050201.checkins_super, Gowalla050201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050201' + str(K)


class Gowalla05020112(Gowalla050201):
    K = 12
    checkins = '_'.join([Gowalla050201.checkins_super, Gowalla050201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050201' + str(K)


class Gowalla05020115(Gowalla050201):
    K = 15
    checkins = '_'.join([Gowalla050201.checkins_super, Gowalla050201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050201' + str(K)


class Gowalla05020117(Gowalla050201):
    K = 17
    checkins = '_'.join([Gowalla050201.checkins_super, Gowalla050201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050201' + str(K)


class Gowalla05020120(Gowalla050201):
    K = 20
    checkins = '_'.join([Gowalla050201.checkins_super, Gowalla050201.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050201' + str(K)


class Gowalla050202(Gowalla0502):
    checkins_super = Gowalla0502.checkins.name
    k_anonymity_method = 'EnhancedCADSA'
    max_cached_time = 3600


class Gowalla05020203(Gowalla050202):
    K = 3
    checkins = '_'.join([Gowalla050202.checkins_super, Gowalla050202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0502020' + str(K)


class Gowalla05020205(Gowalla050202):
    K = 5
    checkins = '_'.join([Gowalla050202.checkins_super, Gowalla050202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0502020' + str(K)


class Gowalla05020207(Gowalla050202):
    K = 7
    checkins = '_'.join([Gowalla050202.checkins_super, Gowalla050202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla0502020' + str(K)


class Gowalla05020210(Gowalla050202):
    K = 10
    checkins = '_'.join([Gowalla050202.checkins_super, Gowalla050202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050202' + str(K)


class Gowalla05020212(Gowalla050202):
    K = 12
    checkins = '_'.join([Gowalla050202.checkins_super, Gowalla050202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050202' + str(K)


class Gowalla05020215(Gowalla050202):
    K = 15
    checkins = '_'.join([Gowalla050202.checkins_super, Gowalla050202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050202' + str(K)


class Gowalla05020217(Gowalla050202):
    K = 17
    checkins = '_'.join([Gowalla050202.checkins_super, Gowalla050202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050202' + str(K)


class Gowalla05020220(Gowalla050202):
    K = 20
    checkins = '_'.join([Gowalla050202.checkins_super, Gowalla050202.k_anonymity_method, 'K' + str(K)])
    name = 'Gowalla050202' + str(K)
#
#
# class Gowalla0503(Gowalla0501):
#     cluster_num = 300
#     name = 'Gowalla0503'
#     dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
#     url = 'sqlite:///' + dbfilepath
#
#
# class Gowalla050301(Gowalla0503):
#     checkins_super = Gowalla0503.checkins.name
#     k_anonymity_method = 'EnhancedDLS'
#
#
# class Gowalla05030103(Gowalla050301):
#     K = 3
#     checkins = '_'.join([Gowalla050301.checkins_super, Gowalla050301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0503010' + str(K)
#
#
# class Gowalla05030105(Gowalla050301):
#     K = 5
#     checkins = '_'.join([Gowalla050301.checkins_super, Gowalla050301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0503010' + str(K)
#
#
# class Gowalla05030107(Gowalla050301):
#     K = 7
#     checkins = '_'.join([Gowalla050301.checkins_super, Gowalla050301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0503010' + str(K)
#
#
# class Gowalla05030110(Gowalla050301):
#     K = 10
#     checkins = '_'.join([Gowalla050301.checkins_super, Gowalla050301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla050301' + str(K)
#
#
# class Gowalla050301112(Gowalla050301):
#     K = 12
#     checkins = '_'.join([Gowalla050301.checkins_super, Gowalla050301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla050301' + str(K)
#
#
# class Gowalla05030115(Gowalla050301):
#     K = 15
#     checkins = '_'.join([Gowalla050301.checkins_super, Gowalla050301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla050301' + str(K)
#
#
# class Gowalla05030117(Gowalla050301):
#     K = 17
#     checkins = '_'.join([Gowalla050301.checkins_super, Gowalla050301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla050301' + str(K)
#
#
# class Gowalla05030120(Gowalla050301):
#     K = 20
#     checkins = '_'.join([Gowalla050301.checkins_super, Gowalla050301.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla050301' + str(K)
#
#
# class Gowalla050302(Gowalla0503):
#     checkins_super = Gowalla0503.checkins.name
#     k_anonymity_method = 'EnhancedCADSA'
#     max_cached_time = 3600
#
#
# class Gowalla05030203(Gowalla050302):
#     K = 3
#     checkins = '_'.join([Gowalla050302.checkins_super, Gowalla050302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0503020' + str(K)
#
#
# class Gowalla05030205(Gowalla050302):
#     K = 5
#     checkins = '_'.join([Gowalla050302.checkins_super, Gowalla050302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0503020' + str(K)
#
#
# class Gowalla05030207(Gowalla050302):
#     K = 7
#     checkins = '_'.join([Gowalla050302.checkins_super, Gowalla050302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla0503020' + str(K)
#
#
# class Gowalla05030210(Gowalla050302):
#     K = 10
#     checkins = '_'.join([Gowalla050302.checkins_super, Gowalla050302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla050302' + str(K)
#
#
# class Gowalla05030212(Gowalla050302):
#     K = 12
#     checkins = '_'.join([Gowalla050302.checkins_super, Gowalla050302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla050302' + str(K)
#
#
# class Gowalla05030215(Gowalla050302):
#     K = 15
#     checkins = '_'.join([Gowalla050302.checkins_super, Gowalla050302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla050302' + str(K)
#
#
# class Gowalla05030217(Gowalla050302):
#     K = 17
#     checkins = '_'.join([Gowalla050302.checkins_super, Gowalla050302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla050302' + str(K)
#
#
# class Gowalla05030220(Gowalla050302):
#     K = 20
#     checkins = '_'.join([Gowalla050302.checkins_super, Gowalla050302.k_anonymity_method, 'K' + str(K)])
#     name = 'Gowalla050302' + str(K)
#
#
# class SNAPGowalla(Dataset1):
#     checkins = 'Checkins'
#     csvs = {'checkins': 'D:\\Workspace\\Datasets\\Location-Based Social Network\\SNAP Gowalla\\checkins.txt',
#             'edges': 'D:\\Workspace\\Datasets\\Location-Based Social Network\\SNAP Gowalla\\edges.txt'}
#     edges = 'Edges'
#     name = 'SNAPGowalla'
#     ranges = [-180.0, 180.0, -80.0, 80.0]
#     url = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\SNAP Gowalla\\checkins.db'
#
#
# class SNAPGowallaAustin(SNAPGowalla):
#     checkins = 'Checkins_Austin_Time_Sample3600_Length100_Cluster50'
#     edges = 'Edges_Austin_Time_Sample3600_Length100_Cluster50'
#     name = 'SNAPGowalla_Austin'
#     ranges = [-97.7714033167, -97.5977249833, 30.19719445, 30.4448463144]
#
#
# class SNAPGowallaAustinSQLAlchemy(SNAPGowallaAustin):
#     checkins = 'checkins'
#     edges = 'edges'
#     name = 'SNAPGowalla_Audtin_SQLAlchemy'
#     url = 'sqlite:///D:\\Workspace\\Datasets\\Location-Based Social Network\\SNAP Gowalla\\checkins_sqlalchemy.db'
#
#
# class SNAPGowallaPreview(SNAPGowalla):
#     checkins = 'Checkins_Preview'
#     edges = 'Edges_Preview'
#     name = 'SNAPGowalla_Preview'
#
#
# class SNAPGowallaStockholm(SNAPGowalla):
#     checkins = 'Checkins_Stockholm_Time_Sample3600_Length100_Cluster50'
#     edges = 'Edges_Stockholm_Time_Sample3600_Length100_Cluster50'
#     name = 'SNAPGowalla_Stockholm'
#     ranges = [17.911736377, 18.088630197, 59.1932443, 59.4409599167]
#
#
# class SNAPGowallaSanfrancisco(SNAPGowalla):
#     checkins = 'Checkins_SF_Time_Sample3600_Length100_Cluster50'
#     edges = 'Edges_SF_Time_Sample3600_Length100_Cluster50'
#     name = 'SNAPGowalla_Sanfrancisco'
#     ranges = [-122.521368, -122.356684, 37.706357, 37.817344]
#
#
# class SNAPGowallaAustinDLSK5M5(SNAPGowallaAustin):
#     k = 5
#     m = 5
#     checkins = 'Checkins_Stockholm_Time_Sample3600_Length50_Cluster50_DLS_K5_M5'
#     edges = 'Edges_Stockholm_Time_Sample3600_Length100_Cluster50'
#     name = 'SNAPGowalla_Austin_KAnonymous_DLS_K5_M5'
#
#
# class Gowalla0101(Gowalla):
#     Base = declarative_base()
#     edges = Table('edges',
#                   Base.metadata,
#                   Column('userid', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
#                          primary_key=True, index=True),
#                   Column('friendid', Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
#                          primary_key=True, index=True))
#
#     class User(Base):
#         __tablename__ = 'users'
#
#         id = Column(Integer, primary_key=True, index=True)
#         global_userid = Column(Integer, unique=True, index=True)
#
#         followers = relationship('User',
#                                  secondary='edges',
#                                  primaryjoin='User.id==edges.c.userid',
#                                  secondaryjoin='User.id==edges.c.friendid',
#                                  back_populates='followees',
#                                  passive_deletes=True)
#         followees = relationship('User',
#                                  secondary='edges',
#                                  primaryjoin='User.id==edges.c.friendid',
#                                  secondaryjoin='User.id==edges.c.userid',
#                                  back_populates='followers',
#                                  passive_deletes=True)
#         locations = relationship('Location',
#                                  secondary='checkins',
#                                  primaryjoin='User.id==checkins.c.userid',
#                                  secondaryjoin='checkins.c.locid==Location.id',
#                                  back_populates='visitors',
#                                  passive_deletes=True)
#         checkins = relationship('Checkin',
#                                 back_populates='user',
#                                 passive_deletes=True)
#
#     class Location(Base):
#         __tablename__ = 'locations'
#         # __table_args__ = (UniqueConstraint('lon', 'lat', name='gps'),)
#
#         id = Column(Integer, primary_key=True, index=True)
#
#         visitors = relationship('User',
#                                 secondary='checkins',
#                                 primaryjoin='Location.id==checkins.c.locid',
#                                 secondaryjoin='User.id==checkins.c.userid',
#                                 back_populates='locations',
#                                 passive_deletes=True)
#         checkins = relationship('Checkin',
#                                 back_populates='location',
#                                 passive_deletes=True)
#
#     class Checkin(Base):
#         __tablename__ = 'checkins'
#
#         id = Column(Integer, primary_key=True)  # auto_increment=False
#         userid = Column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
#         locdatetime = Column(DateTime, index=True)
#         lon = Column(REAL, index=True)
#         lat = Column(REAL, index=True)
#         locid = Column(Integer, ForeignKey('locations.id', ondelete='CASCADE'), index=True)
#         gridlon = Column(Integer, index=True, nullable=True)  # new
#         gridlat = Column(Integer, index=True, nullable=True)  # new
#         gridid = Column(Integer, index=True, nullable=True)  # new
#         clstlon = Column(REAL, index=True, nullable=True)  # new
#         clstlat = Column(REAL, index=True, nullable=True)  # new
#         clstid = Column(Integer, index=True, nullable=True)  # new
#
#         user = relationship('User',
#                             back_populates='checkins',
#                             passive_deletes=True)
#         location = relationship('Location',
#                                 back_populates='checkins',
#                                 passive_deletes=True)
#
#     checkins = Checkin.__table__
#     cluster_method = 'k-means'
#     cluster_num = 50
#     datetime_range = [datetime(2009, 1, 21, 16, 40, 55), datetime(2011, 8, 16, 18, 54, 25)]  # all datetimes
#     name = 'Gowalla0101'
#     dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
#     locations = Location.__table__
#     min_tracelength = 200
#     ranges = [-99.436238, -94.402017, 28.270606, 34.000000]  # Dallas & Austin & Huston & San Antonio, US
#     gridmap = GridMap(ranges=ranges, granularity=[0.00522254, 0.00220454])  # 500m x 500m  # 482km x 1299km
#     subsample_rate = 1  # seconds, 1 means no subsample will be taken.
#     timezone_offset = -5  # local time = UTC - 5 hours
#     url = 'sqlite:///' + dbfilepath
#     users = User.__table__
#
#
# class Gowalla010103(Gowalla0101):
#     K = 3
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0101.checkins.name
#     checkins = Gowalla0101.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010103'
#
#
# class Gowalla010104(Gowalla0101):
#     K = 4
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0101.checkins.name
#     checkins = Gowalla0101.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010104'
#
#
# class Gowalla010105(Gowalla0101):
#     K = 5
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0101.checkins.name
#     checkins = Gowalla0101.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010105'
#
#
# class Gowalla010106(Gowalla0101):
#     K = 6
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0101.checkins.name
#     checkins = Gowalla0101.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010106'
#
#
# class Gowalla010107(Gowalla0101):
#     K = 7
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0101.checkins.name
#     checkins = Gowalla0101.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010107'
#
#
# class Gowalla010108(Gowalla0101):
#     K = 8
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0101.checkins.name
#     checkins = Gowalla0101.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010108'
#
#
# class Gowalla010109(Gowalla0101):
#     K = 9
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0101.checkins.name
#     checkins = Gowalla0101.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010109'
#
#
# class Gowalla010110(Gowalla0101):
#     K = 10
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0101.checkins.name
#     checkins = Gowalla0101.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010110'
#
#
# class Gowalla010111(Gowalla0101):
#     K = 11
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0101.checkins.name
#     checkins = Gowalla0101.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010111'
#
#
# class Gowalla010112(Gowalla0101):
#     K = 12
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0101.checkins.name
#     checkins = Gowalla0101.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010112'
#
#
# class Gowalla0102(Gowalla0101):
#     cluster_num = 100
#     name = 'Gowalla0102'
#     dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
#     url = 'sqlite:///' + dbfilepath
#
#
# class Gowalla010203(Gowalla0102):
#     K = 3
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0102.checkins.name
#     checkins = Gowalla0102.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010203'
#
#
# class Gowalla010204(Gowalla0102):
#     K = 4
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0102.checkins.name
#     checkins = Gowalla0102.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010204'
#
#
# class Gowalla010205(Gowalla0102):
#     K = 5
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0102.checkins.name
#     checkins = Gowalla0102.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010205'
#
#
# class Gowalla010206(Gowalla0102):
#     K = 6
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0102.checkins.name
#     checkins = Gowalla0102.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010206'
#
#
# class Gowalla010207(Gowalla0102):
#     K = 7
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0102.checkins.name
#     checkins = Gowalla0102.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010207'
#
#
# class Gowalla010208(Gowalla0102):
#     K = 8
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0102.checkins.name
#     checkins = Gowalla0102.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010208'
#
#
# class Gowalla010209(Gowalla0102):
#     K = 9
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0102.checkins.name
#     checkins = Gowalla0102.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010209'
#
#
# class Gowalla010210(Gowalla0102):
#     K = 10
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0102.checkins.name
#     checkins = Gowalla0102.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010210'
#
#
# class Gowalla010211(Gowalla0102):
#     K = 11
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0102.checkins.name
#     checkins = Gowalla0102.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010211'
#
#
# class Gowalla010212(Gowalla0102):
#     K = 12
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0102.checkins.name
#     checkins = Gowalla0102.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010212'
#
#
# class Gowalla010213(Gowalla0102):
#     K = 13
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0102.checkins.name
#     checkins = Gowalla0102.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010213'
#
#
# class Gowalla010214(Gowalla0102):
#     K = 14
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0102.checkins.name
#     checkins = Gowalla0102.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010214'
#
#
# class Gowalla010215(Gowalla0102):
#     K = 15
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0102.checkins.name
#     checkins = Gowalla0102.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010215'
#
#
# class Gowalla010216(Gowalla0102):
#     K = 16
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0102.checkins.name
#     checkins = Gowalla0102.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010216'
#
#
# class Gowalla010217(Gowalla0102):
#     K = 17
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0102.checkins.name
#     checkins = Gowalla0102.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010217'
#
#
# class Gowalla010218(Gowalla0102):
#     K = 18
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0102.checkins.name
#     checkins = Gowalla0102.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010218'
#
#
# class Gowalla010219(Gowalla0102):
#     K = 19
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0102.checkins.name
#     checkins = Gowalla0102.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010219'
#
#
# class Gowalla010220(Gowalla0102):
#     K = 20
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0102.checkins.name
#     checkins = Gowalla0102.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010220'
#
#
# class Gowalla0103(Gowalla0101):
#     cluster_num = 150
#     name = 'Gowalla0103'
#     dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
#     url = 'sqlite:///' + dbfilepath
#
#
# class Gowalla010303(Gowalla0103):
#     K = 3
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0103.checkins.name
#     checkins = Gowalla0103.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010303'
#
#
# class Gowalla010304(Gowalla0103):
#     K = 4
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0103.checkins.name
#     checkins = Gowalla0103.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010304'
#
#
# class Gowalla010305(Gowalla0103):
#     K = 5
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0103.checkins.name
#     checkins = Gowalla0103.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010305'
#
#
# class Gowalla010306(Gowalla0103):
#     K = 6
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0103.checkins.name
#     checkins = Gowalla0103.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010306'
#
#
# class Gowalla010307(Gowalla0103):
#     K = 7
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0103.checkins.name
#     checkins = Gowalla0103.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010307'
#
#
# class Gowalla010308(Gowalla0103):
#     K = 8
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0103.checkins.name
#     checkins = Gowalla0103.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010308'
#
#
# class Gowalla010309(Gowalla0103):
#     K = 9
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0103.checkins.name
#     checkins = Gowalla0103.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010309'
#
#
# class Gowalla010310(Gowalla0103):
#     K = 10
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0103.checkins.name
#     checkins = Gowalla0103.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010310'
#
#
# class Gowalla010311(Gowalla0103):
#     K = 11
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0103.checkins.name
#     checkins = Gowalla0103.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010311'
#
#
# class Gowalla010312(Gowalla0103):
#     K = 12
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0103.checkins.name
#     checkins = Gowalla0103.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010312'
#
#
# class Gowalla010313(Gowalla0103):
#     K = 13
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0103.checkins.name
#     checkins = Gowalla0103.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010313'
#
#
# class Gowalla010314(Gowalla0103):
#     K = 14
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0103.checkins.name
#     checkins = Gowalla0103.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010314'
#
#
# class Gowalla010315(Gowalla0103):
#     K = 15
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0103.checkins.name
#     checkins = Gowalla0103.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010315'
#
#
# class Gowalla010316(Gowalla0103):
#     K = 16
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0103.checkins.name
#     checkins = Gowalla0103.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010316'
#
#
# class Gowalla010317(Gowalla0103):
#     K = 17
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0103.checkins.name
#     checkins = Gowalla0103.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010317'
#
#
# class Gowalla010318(Gowalla0103):
#     K = 18
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0103.checkins.name
#     checkins = Gowalla0103.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010318'
#
#
# class Gowalla010319(Gowalla0103):
#     K = 19
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0103.checkins.name
#     checkins = Gowalla0103.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010319'
#
#
# class Gowalla010320(Gowalla0103):
#     K = 20
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0103.checkins.name
#     checkins = Gowalla0103.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010320'
#
#
# class Gowalla0104(Gowalla0101):
#     cluster_num = 200
#     name = 'Gowalla0104'
#     dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
#     url = 'sqlite:///' + dbfilepath
#
#
# class Gowalla010403(Gowalla0104):
#     K = 3
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0104.checkins.name
#     checkins = Gowalla0104.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010403'
#
#
# class Gowalla010404(Gowalla0104):
#     K = 4
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0104.checkins.name
#     checkins = Gowalla0104.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010404'
#
#
# class Gowalla010405(Gowalla0104):
#     K = 5
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0104.checkins.name
#     checkins = Gowalla0104.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010405'
#
#
# class Gowalla010406(Gowalla0104):
#     K = 6
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0104.checkins.name
#     checkins = Gowalla0104.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010406'
#
#
# class Gowalla010407(Gowalla0104):
#     K = 7
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0104.checkins.name
#     checkins = Gowalla0104.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010407'
#
#
# class Gowalla010408(Gowalla0104):
#     K = 8
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0104.checkins.name
#     checkins = Gowalla0104.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010408'
#
#
# class Gowalla010409(Gowalla0104):
#     K = 9
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0104.checkins.name
#     checkins = Gowalla0104.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010409'
#
#
# class Gowalla010410(Gowalla0104):
#     K = 10
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0104.checkins.name
#     checkins = Gowalla0104.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010410'
#
#
# class Gowalla010411(Gowalla0104):
#     K = 11
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0104.checkins.name
#     checkins = Gowalla0104.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010411'
#
#
# class Gowalla010412(Gowalla0104):
#     K = 12
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0104.checkins.name
#     checkins = Gowalla0104.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010412'
#
#
# class Gowalla010413(Gowalla0104):
#     K = 13
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0104.checkins.name
#     checkins = Gowalla0104.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010413'
#
#
# class Gowalla010414(Gowalla0104):
#     K = 14
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0104.checkins.name
#     checkins = Gowalla0104.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010414'
#
#
# class Gowalla010415(Gowalla0104):
#     K = 15
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0104.checkins.name
#     checkins = Gowalla0104.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010415'
#
#
# class Gowalla010416(Gowalla0104):
#     K = 16
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0104.checkins.name
#     checkins = Gowalla0104.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010416'
#
#
# class Gowalla010417(Gowalla0104):
#     K = 17
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0104.checkins.name
#     checkins = Gowalla0104.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010417'
#
#
# class Gowalla010418(Gowalla0104):
#     K = 18
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0104.checkins.name
#     checkins = Gowalla0104.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010418'
#
#
# class Gowalla010419(Gowalla0104):
#     K = 19
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0104.checkins.name
#     checkins = Gowalla0104.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010419'
#
#
# class Gowalla010420(Gowalla0104):
#     K = 20
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0104.checkins.name
#     checkins = Gowalla0104.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010420'
#
#
# class Gowalla0105(Gowalla0101):
#     cluster_num = 500
#     name = 'Gowalla0105'
#     dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
#     url = 'sqlite:///' + dbfilepath
#
#
# class Gowalla010503(Gowalla0105):
#     K = 3
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0105.checkins.name
#     checkins = Gowalla0105.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010503'
#
#
# class Gowalla010505(Gowalla0105):
#     K = 5
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0105.checkins.name
#     checkins = Gowalla0105.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010505'
#
#
# class Gowalla010510(Gowalla0105):
#     K = 10
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0105.checkins.name
#     checkins = Gowalla0105.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010510'
#
#
# class Gowalla010515(Gowalla0105):
#     K = 15
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0105.checkins.name
#     checkins = Gowalla0105.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010515'
#
#
# class Gowalla0106(Gowalla0101):
#     cluster_num = 1000
#     name = 'Gowalla0106'
#     dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
#     url = 'sqlite:///' + dbfilepath
#
#
# class Gowalla010603(Gowalla0106):
#     K = 3
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0106.checkins.name
#     checkins = Gowalla0106.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010603'
#
#
# class Gowalla010605(Gowalla0106):
#     K = 5
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0106.checkins.name
#     checkins = Gowalla0106.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010605'
#
#
# class Gowalla010610(Gowalla0106):
#     K = 10
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0106.checkins.name
#     checkins = Gowalla0106.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010610'
#
#
# class Gowalla010615(Gowalla0106):
#     K = 15
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0106.checkins.name
#     checkins = Gowalla0106.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla010615'
#
#
# class Gowalla0111(Gowalla0101):
#     name = 'Gowalla0111'
#     dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
#     subsample_rate = 1800
#     url = 'sqlite:///' + dbfilepath
#
#
# class Gowalla011103(Gowalla0111):
#     K = 3
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0111.checkins.name
#     checkins = Gowalla0111.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla011103'
#
#
# class Gowalla011105(Gowalla0111):
#     K = 5
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0111.checkins.name
#     checkins = Gowalla0111.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla011105'
#
#
# class Gowalla011110(Gowalla0111):
#     K = 10
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0111.checkins.name
#     checkins = Gowalla0111.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla011110'
#
#
# class Gowalla0112(Gowalla0101):
#     name = 'Gowalla0112'
#     dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
#     subsample_rate = 3600
#     url = 'sqlite:///' + dbfilepath
#
#
# class Gowalla011203(Gowalla0112):
#     K = 3
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0112.checkins.name
#     checkins = Gowalla0112.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla011203'
#
#
# class Gowalla011205(Gowalla0112):
#     K = 5
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0112.checkins.name
#     checkins = Gowalla0112.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla011205'
#
#
# class Gowalla011210(Gowalla0112):
#     K = 10
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0112.checkins.name
#     checkins = Gowalla0112.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla011210'
#
#
# class Gowalla0121(Gowalla0101):
#     cluster_num = 100
#     name = 'Gowalla0121'
#     dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
#     subsample_rate = 1800
#     url = 'sqlite:///' + dbfilepath
#
#
# class Gowalla012103(Gowalla0121):
#     K = 3
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0121.checkins.name
#     checkins = Gowalla0121.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012103'
#
#
# class Gowalla012105(Gowalla0121):
#     K = 5
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0121.checkins.name
#     checkins = Gowalla0121.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012105'
#
#
# class Gowalla012110(Gowalla0121):
#     K = 10
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0121.checkins.name
#     checkins = Gowalla0121.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012110'
#
#
# class Gowalla012115(Gowalla0121):
#     K = 15
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0121.checkins.name
#     checkins = Gowalla0121.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012115'
#
#
# class Gowalla012120(Gowalla0121):
#     K = 20
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0121.checkins.name
#     checkins = Gowalla0121.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012120'
#
#
# class Gowalla0122(Gowalla0101):
#     cluster_num = 100
#     name = 'Gowalla0122'
#     dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
#     subsample_rate = 3600
#     url = 'sqlite:///' + dbfilepath
#
#
# class Gowalla012203(Gowalla0122):
#     K = 3
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0122.checkins.name
#     checkins = Gowalla0122.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012203'
#
#
# class Gowalla012205(Gowalla0122):
#     K = 5
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0122.checkins.name
#     checkins = Gowalla0122.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012205'
#
#
# class Gowalla012210(Gowalla0122):
#     K = 10
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0122.checkins.name
#     checkins = Gowalla0122.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012210'
#
#
# class Gowalla012215(Gowalla0122):
#     K = 15
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0122.checkins.name
#     checkins = Gowalla0122.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012215'
#
#
# class Gowalla012220(Gowalla0122):
#     K = 20
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0122.checkins.name
#     checkins = Gowalla0122.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012220'
#
#
# class Gowalla0124(Gowalla0101):
#     cluster_num = 200
#     name = 'Gowalla0124'
#     dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
#     subsample_rate = 1800
#     url = 'sqlite:///' + dbfilepath
#
#
# class Gowalla012403(Gowalla0124):
#     K = 3
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0124.checkins.name
#     checkins = Gowalla0124.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012403'
#
#
# class Gowalla012405(Gowalla0124):
#     K = 5
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0124.checkins.name
#     checkins = Gowalla0124.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012405'
#
#
# class Gowalla012410(Gowalla0124):
#     K = 10
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0124.checkins.name
#     checkins = Gowalla0124.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012410'
#
#
# class Gowalla012415(Gowalla0124):
#     K = 15
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0124.checkins.name
#     checkins = Gowalla0124.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012415'
#
#
# class Gowalla012420(Gowalla0124):
#     K = 20
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0124.checkins.name
#     checkins = Gowalla0124.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012420'
#
#
# class Gowalla0125(Gowalla0101):
#     cluster_num = 200
#     name = 'Gowalla0125'
#     dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
#     subsample_rate = 3600
#     url = 'sqlite:///' + dbfilepath
#
#
# class Gowalla012503(Gowalla0125):
#     K = 3
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0125.checkins.name
#     checkins = Gowalla0125.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012503'
#
#
# class Gowalla012505(Gowalla0125):
#     K = 5
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0125.checkins.name
#     checkins = Gowalla0125.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012505'
#
#
# class Gowalla012510(Gowalla0125):
#     K = 10
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0125.checkins.name
#     checkins = Gowalla0125.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012510'
#
#
# class Gowalla012515(Gowalla0125):
#     K = 15
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0125.checkins.name
#     checkins = Gowalla0125.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012515'
#
#
# class Gowalla012520(Gowalla0125):
#     K = 20
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0125.checkins.name
#     checkins = Gowalla0125.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla012520'
#
#
# class Gowalla0131(Gowalla0101):
#     cluster_num = 50
#     min_tracelength = 100
#     name = 'Gowalla0131'
#     dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
#     url = 'sqlite:///' + dbfilepath
#
#
# class Gowalla013103(Gowalla0131):
#     K = 3
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0131.checkins.name
#     checkins = Gowalla0131.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla013103'
#
#
# class Gowalla013105(Gowalla0131):
#     K = 5
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0131.checkins.name
#     checkins = Gowalla0131.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla013105'
#
#
# class Gowalla013110(Gowalla0131):
#     K = 10
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0131.checkins.name
#     checkins = Gowalla0131.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla013110'
#
#
# class Gowalla0132(Gowalla0101):
#     cluster_num = 50
#     min_tracelength = 300
#     name = 'Gowalla0132'
#     dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
#     url = 'sqlite:///' + dbfilepath
#
#
# class Gowalla013203(Gowalla0132):
#     K = 3
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0132.checkins.name
#     checkins = Gowalla0132.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla013203'
#
#
# class Gowalla013205(Gowalla0132):
#     K = 5
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0132.checkins.name
#     checkins = Gowalla0132.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla013205'
#
#
# class Gowalla013210(Gowalla0132):
#     K = 10
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0132.checkins.name
#     checkins = Gowalla0132.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla013210'
#
#
# class Gowalla0133(Gowalla0101):
#     cluster_num = 50
#     min_tracelength = 500
#     name = 'Gowalla0133'
#     dbfilepath = 'D:\\Workspace\\Datasets\\Location-Based Social Network\\Gowalla\\' + name + '.db'
#     url = 'sqlite:///' + dbfilepath
#
#
# class Gowalla013303(Gowalla0133):
#     K = 3
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0133.checkins.name
#     checkins = Gowalla0133.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla013303'
#
#
# class Gowalla013305(Gowalla0133):
#     K = 5
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0133.checkins.name
#     checkins = Gowalla0133.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla013305'
#
#
# class Gowalla013310(Gowalla0132):
#     K = 10
# #     k_anonymity_method = '_EnhancedDLS'
#     checkins_super = Gowalla0133.checkins.name
#     checkins = Gowalla0133.checkins.name + k_anonymity_method + '_K' + str(K) + '_M' + str(M)
#     name = 'Gowalla013310'
