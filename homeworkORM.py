import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm  import sessionmaker, relationship
from sqlalchemy import func
from pprint import pprint
import pandas as pd

from sqlalchemy.orm.util import join
from sqlalchemy.sql.selectable import subquery

Base = declarative_base()

engine = sq.create_engine('postgresql+psycopg2://**********:***********@localhost:5432/postgres')
Session = sessionmaker(bind=engine)

class Genre(Base):
    __tablename__ = "genre"

    id = sq.Column(sq.Integer, primary_key=True)
    genre_name = sq.Column(sq.String, nullable=False, unique=True)
    executors = relationship('Executor', secondary='genre_executor', back_populates='genres', cascade="all,delete", cascade_backrefs=True)


genre_executor = sq.Table(
 'genre_executor', Base.metadata,
 sq.Column('genre_id', sq.Integer, sq.ForeignKey('genre.id')),
 sq.Column('executor_id', sq.Integer, sq.ForeignKey('executor.id'))
)


class Executor(Base):
    __tablename__ = "executor"

    id = sq.Column(sq.Integer, primary_key=True)
    executor_name = sq.Column(sq.String, nullable=False)
    genres = relationship(Genre, secondary=genre_executor, back_populates='executors', cascade="all,delete")
    albums = relationship('Album', secondary='executor_album', back_populates='executors', cascade="all,delete", cascade_backrefs=True)


executor_album = sq.Table(
 'executor_album', Base.metadata,
 sq.Column('executor_id', sq.Integer, sq.ForeignKey('executor.id')),
 sq.Column('album_id', sq.Integer, sq.ForeignKey('album.id'))
)


class Album(Base):
    __tablename__ = "album"

    id = sq.Column(sq.Integer, primary_key=True)
    album_name = sq.Column(sq.String, nullable=False)
    year_of_release = sq.Column(sq.Integer, nullable=False)
    tracks = relationship('Track', backref='album')
    executors = relationship(Executor, secondary=executor_album, back_populates='albums', cascade="all,delete")


class Track(Base):
    __tablename__ = "track"

    id = sq.Column(sq.Integer, primary_key=True)
    track_name = sq.Column(sq.String, nullable=False, unique=True)
    duration = sq.Column(sq.Integer, nullable=False)
    id_album = sq.Column(sq.Integer, sq.ForeignKey('album.id'))
    collections = relationship('Collection', secondary='collection_track', back_populates='tracks', cascade="all,delete", cascade_backrefs=True)


collection_track = sq.Table(
 'collection_track', Base.metadata,
 sq.Column('track_id', sq.Integer, sq.ForeignKey('track.id')),
 sq.Column('collection_id', sq.Integer, sq.ForeignKey('collection_of_songs.id'))
)


class Collection(Base):
    __tablename__ = "collection_of_songs"
    
    id = sq.Column(sq.Integer, primary_key=True)
    collection_name = sq.Column(sq.String, nullable=False, unique=True)
    year_of_release = sq.Column(sq.Integer, nullable=False)
    tracks = relationship(Track, secondary=collection_track, back_populates='collections', cascade="all,delete")


my_data = {
"Jazz": {
    'Frank Sinatra': [
        'My Way', 1969, (
            {'name': 'Watch What Happens', 'dur': 141},
            {'name': 'My Way', 'dur': 277}
        )
    ],
    'Louis Armstrong': [
        'What a Wonderful World', 1967, (
            {'name': 'What a Wonderful World', 'dur': 140},
            {'name': 'Hello Brother', 'dur': 212}
        )
    ]    
},
'Rap': {
    'Баста': [
        'Баста 40', 2020, (
            {'name': '+100500', 'dur': 348},
            {'name': 'Любовь и страх', 'dur': 320},
            {'name': 'Белый кит', 'dur': 320}
        )
    ],
    'Eminem': [
        'Music To Be Murdered By - Side B', 2020, (
            {'name': 'Killer', 'dur': 195},
            {'name': 'No Regrets', 'dur': 201},
            {'name': 'Gnat', 'dur': 225}
        )
    ]
},
'Rnb': {
    'Chris Brouwn': [
        'Indigo', 2019, (
            {'name': 'No Guidance', 'dur': 261},
            {'name': 'Dear God', 'dur': 243}
        )
    ]
},
'Pop': {
    'Justin Timberlake': [
        'Man of the Woods', 2018, (
            {'name': 'Supplies', 'dur': 226},
            {'name': 'Say Something', 'dur': 279}
        )
    ]
},
'Rock': {
    'AC/DC': [
        'Back in Black', 1980, (
            {'name': 'Back in Black', 'dur': 256},
            {'name': 'Rock and Rol Ain"t Noise Pollution', 'dur': 256}
        )
    ],
    'Linkin Park': [
        'Living Things', 2012, (
            {'name': 'Burn it Down', 'dur': 230},
            {'name': 'Powerless', 'dur': 225}
        )
    ]
}}
coll_data_list = [
    ('Сборник1', 1970), ('Сборник2', 2014),
 	('Сборник3', 2018), ('Сборник4', 2019),
 	('Сборник5', 2019), ('Сборник6', 2020),
 	('Сборник7', 2020), ('Сборник8', 2020)
    ]

collection_track_list = [
    (1,1), (3,1), (2,2), (4,2), (9,3), (11,3), (10,4), (12,4), 
	(13,5), (15,5), (14,6), (16,6), (5,7), (7,7), (6,8), (8,8)
]

if __name__ == '__main__':
    Base.metadata.create_all(engine) # Create table

    session = Session()

    for collec_data in coll_data_list:
        _collection = Collection(collection_name=collec_data[0], year_of_release=collec_data[1])
        session.add(_collection)
    # 
    for genr, execut in my_data.items():
        _genre = Genre(genre_name=genr)
        session.add(_genre)
        #
        for name_ex, data_alb in execut.items():
            _executor = Executor(executor_name=name_ex)
            session.add(_executor)
            _executor.genres.append(_genre)
            #
            _album = Album(album_name=data_alb[0], year_of_release=data_alb[1])
            session.add(_album)
            _album.executors.append(_executor)
            #
            for data_track in data_alb[2]:
                _track = Track(track_name=data_track['name'], duration=data_track['dur'], album=_album)
                session.add(_track)
                
    for data_id in collection_track_list:
        for _collection in session.query(Collection).filter(Collection.id == data_id[1]):
            for track in session.query(Track).filter(Track.id == data_id[0]):
                track.collections.append(_collection)
            
    gen = session.query(Genre).filter(Genre.genre_name == 'Rnb')
    jus_timber = session.query(Executor).filter(Executor.executor_name == 'Justin Timberlake')
    for g in gen:
        for i in jus_timber:
            i.genres.append(g)

    session.commit()

    '''
    1.количество исполнителей в каждом жанре;
    2.количество треков, вошедших в альбомы 2019-2020 годов;
    3.средняя продолжительность треков по каждому альбому;
    4.все исполнители, которые не выпустили альбомы в 2020 году;
    5.названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
    6.название альбомов, в которых присутствуют исполнители более 1 жанра;
    7.наименование треков, которые не входят в сборники;
    8.исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);
    9.название альбомов, содержащих наименьшее количество треков.
    '''

    count = session.query(Genre.genre_name, (func.count(Executor.id))).join(Genre.executors).group_by(Genre.id)
    # print(list(count))
    co_tr = session.query(Album.album_name, func.count(Track.id)).join(Album.tracks).filter(Album.year_of_release.between(2019, 2020)).group_by(Album.album_name)
    # print(f'\n{list(co_tr)}')
    avg_dur = session.query(Album.album_name, func.avg(Track.duration)).join(Album.tracks).group_by(Album.album_name)
    # print(f'\n{list(avg_dur)}')
    execut = session.query(Executor.executor_name).join(Album.executors).filter(Album.year_of_release==2020)
    # print(f'\n{list(execut)}')
    coll_name = session.query(Collection.collection_name).join(Collection.tracks).join(Album).join(Album.executors).filter(Executor.executor_name == 'Eminem').group_by(Collection.collection_name)
    # print(f'\n{list(coll_name)}')
    name_alb = session.query(Album.album_name).join(Album.executors).join(Executor.genres).having(func.count(Genre.id)>1).group_by(Album.album_name)
    # print(f'\n{list(name_alb)}')
    tr = session.query(func.min(Track.duration)).scalar_subquery()
    ex_name = session.query(Executor.executor_name).join(Executor.albums).join(Album.tracks).filter(Track.duration==tr).group_by(Executor.executor_name)
    # print(f'\n{list(ex_name)}')
    
    subquery1 = session.query(func.count(Track.id)).group_by(Track.id_album).order_by(func.count(Track.id)).limit(1).scalar_subquery()
    subquery2 = session.query(Track.id_album).group_by(Track.id_album).having(func.count(Track.id) == subquery1).scalar_subquery()
    c = session.query(Album.album_name).join(Track).filter(Track.id_album.in_(subquery2)).group_by(Album.album_name)

    # pprint(list(c))
    # al_name = session.query(Album.album_name)
    dataset = pd.DataFrame(c)
    print(dataset)

    print('Finish')



   