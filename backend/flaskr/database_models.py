from flaskr import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String, nullable=False)  # Check constraint handled at application level
    occupation = db.Column(db.String)
    preferred_genre = db.Column(db.String)
    recommended_genre = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String)
    firebase_uid = db.Column(db.String, unique=True)

    def __repr__(self):
        return f'<User {self.email}>'


class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    genres = db.Column(db.String, nullable=False)
    imdb_id = db.Column(db.Integer)
    tmdb_id = db.Column(db.Integer)
    description = db.Column(db.Text)
    release_date = db.Column(db.String)
    poster_path = db.Column(db.String)

    def __repr__(self):
        return f'<Movie {self.title}>'


class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f'<Genre {self.name}>'


class UserWatchlist(db.Model):
    __tablename__ = 'user_watchlist'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    user = db.relationship('User', backref=db.backref('watchlist', lazy=True))
    movie = db.relationship('Movie', backref=db.backref('watchlists', lazy=True))

    def __repr__(self):
        return f'<UserWatchlist user_id={self.user_id}, movie_id={self.movie_id}>'


class UserWatched(db.Model):
    __tablename__ = 'user_watched'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    user = db.relationship('User', backref=db.backref('watched_movies', lazy=True))
    movie = db.relationship('Movie', backref=db.backref('watched', lazy=True))

    def __repr__(self):
        return f'<UserWatched user_id={self.user_id}, movie_id={self.movie_id}>'


class UserRatings(db.Model):
    __tablename__ = 'user_ratings'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # Enforce check at application level
    user = db.relationship('User', backref=db.backref('ratings', lazy=True))
    movie = db.relationship('Movie', backref=db.backref('ratings', lazy=True))

    def __repr__(self):
        return f'<UserRatings user_id={self.user_id}, movie_id={self.movie_id}, rating={self.rating}>'


class UserReviews(db.Model):
    __tablename__ = 'user_reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    review = db.Column(db.Text)
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    movie = db.relationship('Movie', backref=db.backref('reviews', lazy=True))

    def __repr__(self):
        return f'<UserReviews id={self.id}, user_id={self.user_id}, movie_id={self.movie_id}>'


class MovielensMovie(db.Model):
    __tablename__ = 'movielens_movies'

    movie_id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String, nullable=False)
    genres = db.Column(db.String, nullable=False)
    tmdb_id = db.Column(db.Integer)
    imdb_id = db.Column(db.String)


class MovielensRating(db.Model):
    __tablename__ = 'movielens_ratings'

    movie_id = db.Column(db.Integer, primary_key=True)
    movielens_user_id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)
