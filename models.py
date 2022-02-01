from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


venue_genre = db.Table('venue_genre',
                       db.Column('venue_id', db.Integer,
                                 db.ForeignKey('venue.id'), primary_key=True),
                       db.Column('genre_name', db.String(120),
                                 db.ForeignKey('genre.name'), primary_key=True)
                       )


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.relationship('Genre', secondary=venue_genre, lazy='subquery',
                             backref=db.backref('venue', lazy=True))
    facebook_link = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    website_link = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))

    shows = db.relationship('Show', backref='venue', lazy='dynamic')

    def __repr__(self):
        return f'{self.id}: {self.name}'


artist_genre = db.Table('artist_genre',
                        db.Column('artist_id', db.Integer,
                                  db.ForeignKey('artist.id'), primary_key=True),
                        db.Column('genre_name', db.String(120),
                                  db.ForeignKey('genre.name'), primary_key=True)
                        )


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.relationship('Genre', secondary=artist_genre, lazy='subquery',
                             backref=db.backref('artist', lazy=True))
    facebook_link = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    website_link = db.Column(db.String(120), nullable=False)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))

    shows = db.relationship('Show', backref='artist', lazy='dynamic')

    def __repr__(self):
        return f'{self.id}: {self.name}'


class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'),
                         nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'),
                          nullable=False)
    start_time = db.Column(db.DateTime(), nullable=False)


class Genre(db.Model):
    __tablename__ = 'genre'

    name = db.Column(db.String(120), primary_key=True, nullable=False, unique=True)

    def __repr__(self):
        return f'{self.name}'
