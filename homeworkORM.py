import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm  import sessionmaker, relationship
from pprint import pprint

Base = declarative_base()

engine = sq.create_engine('postgresql+psycopg2://*******:*******@localhost:5432/postgres')
Session = sessionmaker(bind=engine)

class Genre(Base):
    __tablename__ = "genre"

    id = sq.Column(sq.Integer, primary_key=True)
    genre_name = sq.Column(sq.String, nullable=False, unique=True)
    executors = relationship('Executor', secondary='genre_executor')


genre_executor = sq.Table(
 'genre_executor', Base.metadata,
 sq.Column('genre_id', sq.Integer, sq.ForeignKey('genre.id')),
 sq.Column('executor_id', sq.Integer, sq.ForeignKey('executor.id'))
)


class Executor(Base):
    __tablename__ = "executor"

    id = sq.Column(sq.Integer, primary_key=True)
    executor_name = sq.Column(sq.String, nullable=False)
    genres = relationship(Genre, secondary=genre_executor)
    albums = relationship('Album', secondary='executor_album')


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
    executors = relationship(Executor, secondary=executor_album)


class Track(Base):
    __tablename__ = "track"

    id = sq.Column(sq.Integer, primary_key=True)
    track_name = sq.Column(sq.String, nullable=False, unique=True)
    duration = sq.Column(sq.Integer, nullable=False)
    id_album = sq.Column(sq.Integer, sq.ForeignKey('album.id'))
#     collections = relationship('Collection', secondary='collection_track')


# collection_track = sq.Table(
#  'collection_track', Base.metadata,
#  sq.Column('track_id', sq.Integer, sq.ForeignKey('track.id')),
#  sq.Column('collection_id', sq.Integer, sq.ForeignKey('collection_of_songs.id'))
# )


# class Collection(Base):
#     __tablename__ = "collection_of_songs"
    
#     id = sq.Column(sq.Integer, primary_key=True)
#     collection_name = sq.Column(sq.String, nullable=False, unique=True)
#     year_of_release = sq.Column(sq.Integer, nullable=False)
#     tracks = relationship(Track, secondary=collection_track)


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


if __name__ == '__main__':
    Base.metadata.create_all(engine) # Create table

    session = Session()

    genre_list = []
    executor_list = []
    album_list = []
    track_list = []

    for genr, execut in my_data.items():
        _genre = Genre(genre_name=genr)
        genre_list.append(_genre)

        for name_ex, data_alb in execut.items():
            _executor = Executor(executor_name=name_ex)
            executor_list.append(_executor)
            _executor.genres.append(_genre)

            _album = Album(album_name=data_alb[0], year_of_release=data_alb[1])
            album_list.append(_album)
            _album.executors.append(_executor)

            for data_track in data_alb[2]:
                _track = Track(track_name=data_track['name'], duration=data_track['dur'], album=_album)
                track_list.append(_track)
                
    session.add_all(genre_list)
    session.add_all(executor_list)
    session.add_all(album_list)
    session.add_all(track_list)
    session.commit()



   