import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

engine = sq.create_engine('postgresql+psycopg2://netology:netology@localhost:5432/music')
Session = sessionmaker(bind=engine)


class Artist(Base):
    __tablename__ = 'artist'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, nullable=False, unique=True)
    albums = relationship('Album', back_populates='artist')


class Album(Base):
    __tablename__ = 'album'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String)
    tracks = relationship('Track', backref='album',  cascade="all,delete")
    published = sq.Column(sq.Date)
    id_artist = sq.Column(sq.Integer, sq.ForeignKey('artist.id'))
    artist = relationship(Artist)


class Genre(Base):
    __tablename__ = 'genre'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String)
    tracks = relationship('Track', secondary='track_to_genre', back_populates='genres', cascade="all,delete", cascade_backrefs=True)


class Track(Base):
    __tablename__ = 'track'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String)
    duration = sq.Column(sq.Integer, nullable=False)
    genres = relationship(Genre, secondary='track_to_genre', back_populates='tracks', cascade="all,delete")
    id_album = sq.Column(sq.Integer, sq.ForeignKey('album.id', ondelete="CASCADE"))
    # artist = relationship('Artist')


track_to_genre = sq.Table(
    'track_to_genre', Base.metadata,
    sq.Column('genre_id', sq.Integer, sq.ForeignKey('genre.id')),
    sq.Column('track_id', sq.Integer, sq.ForeignKey('track.id')),
)


if __name__ == '__main__':
    session = Session()
    # Init scheme
    # Base.metadata.create_all(engine)

    # Example data
    date_ar1 = {
        'Album 1': [
            {'name': 'Track 1_1', 'dur': 60},
            {'name': 'Track 1_2', 'dur': 30},
            {'name': 'Track 1_3', 'dur': 45}
        ],
        'Album 2': [
            {'name': 'Track 2_1', 'dur': 60},
            {'name': 'Track 2_2', 'dur': 30},
            {'name': 'Track 2_3', 'dur': 45}
        ]
    }

    ## Example 1
    # artist_1 = Artist(name="Artist 1")
    # for album_name, album_data in date_ar1.items():
    #     _album = Album(title=album_name, artist=artist_1)
    #     session.add(_album)
    #     tracks = []
    #     for track_data in album_data:
    #         _track = Track(title=track_data['name'], duration=track_data['dur'], album=_album)
    #         tracks.append(_track)
    #     session.add_all(tracks)
    #
    # session.commit()

    # ## Example 2
    # blues = Genre(title='Blues')
    # folk = Genre(title='Folk')
    #
    query_blues = session.query(Track).filter(Track.duration <= 40)
    # tracks_blues = query_blues.all()
    # tracks_folk = session.query(Track).filter_by(id_album=1).filter(Track.duration > 30).all()
    # for _track in tracks_folk:
    #     _track.genres.append(blues)
    #     _track.genres.append(folk)
    #
    # for _track in tracks_blues:
    #     _track.genres.append(blues)
    #
    # query_blues.update({"duration": 35})
    # session.commit()

    print('Finish')
