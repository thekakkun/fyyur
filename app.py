#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import logging
from logging import FileHandler, Formatter

import babel
import dateutil.parser
from flask import (Flask, Response, flash, redirect, render_template, request,
                   url_for)
from flask_migrate import Migrate
from flask_moment import Moment
from flask_wtf import Form
from flask_wtf.csrf import CSRFProtect

from forms import *
from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    venues = Venue.query.order_by(Venue.state, Venue.city).all()
    data = []
    for venue in venues:
        listing = {
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': venue.shows.filter(datetime.now() < Show.start_time).count()
        }
        try:
            if (data[-1]['state'] == venue.state
                    and data[-1]['city'] == venue.city):
                data[-1]['venues'].append(listing)
            else:
                data.append({'city': venue.city,
                             'state': venue.state,
                             'venues': [listing]})
        except IndexError:
            data.append({'city': venue.city,
                         'state': venue.state,
                         'venues': [listing]})

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    keyword = request.form.get('search_term')
    matches = Venue.query.filter(Venue.name.ilike(f'%{keyword}%')).all()
    response = {'count': len(matches), 'data': []}
    for match in matches:
        response['data'].append({'id': match.id,
                                 'name': match.name,
                                 'num_upcoming_shows': match.shows.filter(
                                     datetime.now() < Show.start_time).count()})

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id

    data = Venue.query.get(venue_id)
    data.upcoming_shows = []
    data.upcoming_shows_count = 0
    data.past_shows = []
    data.past_shows_count = 0

    for show in data.shows.all():
        show_data = {
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": str(show.start_time)
        }
        if datetime.now() < show.start_time:
            data.upcoming_shows.append(show_data)
            data.upcoming_shows_count += 1
        else:
            data.past_shows.append(show_data)
            data.past_shows_count += 1

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@ app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@ app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False

    data = request.form
    form = VenueForm(request.form)

    if not form.validate():
        for (field, error) in form.errors.items():
            flash(f'{field}: {error}', 'danger')
        return render_template('forms/new_venue.html', form=form)

    try:
        venue = Venue(name=data.get('name'),
                      city=data.get('city'),
                      state=data.get('state'),
                      address=data.get('address'),
                      phone=data.get('phone'),
                      facebook_link=data.get('facebook_link'),
                      image_link=data.get('image_link'),
                      website_link=data.get('website_link'))

        if data.get('seeking_talent') == 'y':
            venue.seeking_talent = True
            venue.seeking_description = data.get('seeking_description')

        db.session.add(venue)
        db.session.flush()
        venue_id = venue.id
        for genre in data.getlist('genres'):
            if not Genre.query.filter_by(name=genre).all():
                db.session.add(Genre(name=genre))
                db.session.flush()
            db.session.execute(venue_genre.insert(), params={
                               'venue_id': venue_id, 'genre_name': genre})

        db.session.commit()

    except:
        error = True
        db.session.rollback()

    finally:
        db.session.close()

    if error:
        # on unsuccessful db insert, flash an error instead.
        flash(
            f'An error occured: Venue {request.form["name"]} could not be listed.', 'danger')
    else:
        # on successful db insert, flash success
        flash(f'Venue {request.form["name"]} was successfully listed!', 'info')

    return render_template('pages/home.html')


@ app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

    venue = Venue.query.get(venue_id)
    venue_name = venue.name
    error = False
    try:
        db.session.delete(venue)
        db.session.commit()

    except:
        db.session.rollback()
        error = True

    finally:
        db.session.close()

    if error:
        # on unsuccessful artist edit, flash an error instead.
        flash(
            f'An error occured: Venue {venue_name} could not be deleted.', 'danger')
    else:
        # on successful db insert, flash success
        flash(f'Venue {venue_name} was successfully deleted!', 'info')

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------


@ app.route('/artists')
def artists():
    data = [{'id': artist.id,
             'name': artist.name}
            for artist in Artist.query.all()]
    return render_template('pages/artists.html', artists=data)


@ app.route('/artists/search', methods=['POST'])
def search_artists():
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    keyword = request.form.get('search_term')
    matches = Artist.query.filter(Artist.name.ilike(f'%{keyword}%')).all()
    response = {'count': len(matches), 'data': []}
    for match in matches:
        response['data'].append({'id': match.id,
                                 'name': match.name,
                                 'num_upcoming_shows': match.shows.filter(
                                     datetime.now() < Show.start_time).count()})

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@ app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id

    data = Artist.query.get(artist_id)
    data.upcoming_shows = []
    data.upcoming_shows_count = 0
    data.past_shows = []
    data.past_shows_count = 0

    shows = [{'venue_id': show.venue.id,
              'venue_name': show.venue.name,
             'venue_image_link': show.venue.image_link,
              'upcoming': datetime.now() < show.start_time,
              'start_time': str(show.start_time)}
             for show in Show.query.filter_by(artist_id=artist_id).all()]

    for show in shows:
        if show['upcoming']:
            data.upcoming_shows.append(show)
            data.upcoming_shows_count += 1
        else:
            data.past_shows.append(show)
            data.past_shows_count += 1

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@ app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()

    artist = Artist.query.get(artist_id)
    form.genres.data = [x.name for x in artist.genres]
    form.seeking_venue.data = artist.seeking_venue

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@ app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # artist record with ID <artist_id> using the new attributes

    data = request.form

    form = ArtistForm(request.form)
    if not form.validate():
        for (field, error) in form.errors.items():
            flash(f'{field}: {error}', 'danger')
        return render_template('forms/new_artist.html', form=form)

    artist = Artist.query.get(artist_id)
    artist_name = Artist.query.get(artist_id).name
    error = False
    try:
        artist.name = data.get('name')
        artist.city = data.get('city')
        artist.state = data.get('state')
        artist.phone = data.get('phone')
        artist.genres = []
        artist.facebook_link = data.get('facebook_link')
        artist.image_link = data.get('image_link')
        artist.website_link = data.get('website_link')
        artist.seeking_venue = False if (
            data.get('seeking_venue')) is None else True
        artist.seeking_description = data.get('seeking_description')

        for genre in data.getlist('genres'):
            if not Genre.query.filter_by(name=genre).all():
                db.session.add(Genre(name=genre))
                db.session.flush()
            db.session.execute(artist_genre.insert(), params={
                               'artist_id': artist_id, 'genre_name': genre})

        db.session.commit()
    except:
        error = True
        db.session.rollback()

    finally:
        db.session.close()

    if error:
        # on unsuccessful artist edit, flash an error instead.
        flash(
            f'An error occured: Artist {artist_name} could not be edited.', 'danger')
    else:
        # on successful db insert, flash success
        flash(f'Artist {artist_name} was successfully edited!', 'info')

    return redirect(url_for('show_artist', artist_id=artist_id))


@ app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()

    venue = Venue.query.get(venue_id)
    form.genres.data = [x.name for x in venue.genres]
    form.seeking_talent.data = venue.seeking_talent

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@ app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    data = request.form

    form = VenueForm(request.form)
    if not form.validate():
        for (field, error) in form.errors.items():
            flash(f'{field}: {error}', 'danger')
        return render_template('forms/new_venue.html', form=form)

    venue = Venue.query.get(venue_id)
    venue_name = Venue.query.get(venue_id).name
    error = False
    try:
        venue.name = data.get('name')
        venue.city = data.get('city')
        venue.state = data.get('state')
        venue.phone = data.get('phone')
        venue.genres = []
        venue.facebook_link = data.get('facebook_link')
        venue.image_link = data.get('image_link')
        venue.website_link = data.get('website_link')
        venue.seeking_talent = False if (
            data.get('seeking_talent')) is None else True
        venue.seeking_description = data.get('seeking_description')

        for genre in data.getlist('genres'):
            if not Genre.query.filter_by(name=genre).all():
                db.session.add(Genre(name=genre))
                db.session.flush()
            db.session.execute(venue_genre.insert(), params={
                               'venue_id': venue_id, 'genre_name': genre})

        db.session.commit()

    except:
        error = True
        db.session.rollback()

    finally:
        db.session.close()

    if error:
        # on unsuccessful venue edit, flash an error instead.
        flash(
            f'An error occured: Artist {venue_name} could not be edited.', 'danger')
    else:
        # on successful db insert, flash success
        flash(f'Artist {venue_name} was successfully edited!', 'info')

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@ app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@ app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False
    data = request.form

    form = ArtistForm(request.form)
    if not form.validate():
        for (field, error) in form.errors.items():
            flash(f'{field}: {error}', 'danger')
        return render_template('forms/new_artist.html', form=form)

    try:
        

        artist = Artist(name=data.get('name'),
                        city=data.get('city'),
                        state=data.get('state'),
                        phone=data.get('phone'),
                        facebook_link=data.get('facebook_link'),
                        image_link=data.get('image_link'),
                        website_link=data.get('website_link'))

        if data.get('seeking_venue') == 'y':
            artist.seeking_venue = True
            artist.seeking_description = data.get('seeking_description')

        db.session.add(artist)
        db.session.flush()
        artist_id = artist.id
        for genre in data.getlist('genres'):
            if not Genre.query.filter_by(name=genre).all():
                db.session.add(Genre(name=genre))
                db.session.flush()
            db.session.execute(artist_genre.insert(), params={
                               'artist_id': artist_id, 'genre_name': genre})

        db.session.add(artist)
        db.session.commit()

    except:
        error = True
        db.session.rollback()

    finally:
        db.session.close()

    if error:
        # on unsuccessful db insert, flash an error instead.
        flash(
            f'An error occured: Artist {request.form["name"]} could not be listed.', 'danger')
    else:
        # on successful db insert, flash success
        flash(
            f'Artist {request.form["name"]} was successfully listed!', 'info')

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@ app.route('/shows')
def shows():
    # displays list of shows at /shows

    shows = Show.query.order_by(Show.start_time).all()
    data = []
    for show in shows:
        data.append({"venue_id": show.venue_id,
                     "venue_name": show.venue.name,
                     "artist_id": show.artist_id,
                     "artist_name": show.artist.name,
                     "artist_image_link": show.artist.image_link,
                     "start_time": str(show.start_time)})

    return render_template('pages/shows.html', shows=data)


@ app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@ app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False

    try:
        data = request.form
        show = Show(artist_id=data.get('artist_id'), venue_id=data.get(
            'venue_id'), start_time=data.get('start_time'))

        db.session.add(show)
        db.session.commit()

    except:
        error = True
        db.session.rollback()

    finally:
        db.session.close()

    if error:
        # on unsuccessful db insert, flash an error instead.
        flash(
            'An error occurred. Show could not be listed.', 'danger')
    else:
        # on successful db insert, flash success
        flash('Show was successfully listed!', 'info')

    return render_template('pages/home.html')


@ app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@ app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
