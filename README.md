# Fyyur

A project for [Udacity's Full Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044), Part 1: SQL and Data Modeling for the Web.

Check out the [original repo](https://github.com/udacity/cd0046-SQL-and-Data-Modeling-for-the-Web) for more information on the project, or [see the rest of the projects completed for the nanodegree](https://github.com/thekakkun/udacity_projects).

## Tech Stack (Dependencies)

### Backend Dependencies

- **SQLAlchemy ORM** to be our ORM library of choice
- **PostgreSQL** as our database of choice
- **Python3** and **Flask** as our server language and server framework
- **Flask-Migrate** for creating and running schema migrations

### Frontend Dependencies

- **Bootstrap3** as the website's frontend.

## Progress

### Minimum Acceptance Criteria

- [x] Connect to a database in config.py. A project submission that uses a local database connection is fine.
- [x] Using SQLAlchemy, set up normalized models for the objects we support in our web app in the Models section of app.py. Check out the sample pages provided at /artists/1, /venues/1, and /shows for examples of the data we want to model, using all of the learned best practices in database schema design. Implement missing model properties and relationships using database migrations via Flask-Migrate.
- [x] Implement form submissions for creating new Venues, Artists, and Shows. There should be proper constraints, powering the /create endpoints that serve the create form templates, to avoid duplicate or nonsensical form submissions. Submitting a form should create proper new records in the database.
  - [x] populate genre table, create row when adding venues
  - [x] Implement "venue searching for artist"
  - [x] Don't add genre as new row if data already exists in genre table
  - [x] Implement creation of shows
  - [x] Implement correct status for showing seeking status in edit form
  - [x] Saving edit updates genre
  - [x] Show error if unable to save changes
- [x] Implement the controllers for listing venues, artists, and shows. Note the structure of the mock data used. We want to keep the structure of the mock data.
  - [x] Show artist list and artist page
  - [x] Show venue list and venue page
  - [x] Show show list
- [x] Implement search, powering the /search endpoints that serve the application's search functionalities.
- [x] Serve venue and artist detail pages, powering the `<venue|artist>/<id>` endpoints that power the detail pages.

### Feedback after submission:

- [ ] Your migration scripts are not working - please make sure they start from a blank database, i.e. no table in it
- [x] Your requirements.txt does not contain all the dependencies used in your project. Make sure you use "pip freeze > requirements.txt"
- [ ] Your code achieved this part of the functionality without using JOIN queries - which in and of itself are good! To challenge yourself and conform with the rubric, make use of the JOIN query in your next submission.
- [ ] Field validation is not implemented.
- [ ]You would also need to separate the model definition into a separate models.py, as per this rubric requirement.

### Above and Beyond

- [ ] Implement artist availability. An artist can list available times that they can be booked. Restrict venues from being able to create shows with artists during a show time that is outside of their availability.
- [ ] Show Recent Listed Artists and Recently Listed Venues on the homepage, returning results for Artists and Venues sorting by newly created. Limit to the 10 most recently listed items.
- [ ] Implement Search Artists by City and State, and Search Venues by City and State. Searching by "San Francisco, CA" should return all artists or venues in San Francisco, CA.
