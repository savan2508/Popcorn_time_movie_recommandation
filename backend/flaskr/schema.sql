DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS movie;
DROP TABLE IF EXISTS user_watchlist;
DROP TABLE IF EXISTS user_watched;
DROP TABLE IF EXISTS genre;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    age INTEGER,
    gender TEXT CHECK(gender IN ('Male', 'Female')) NOT NULL,
    occupation TEXT,
    preferred_genre TEXT,
    recommended_genre TEXT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT,
    firebase_uid TEXT UNIQUE
);

CREATE TABLE movie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genres TEXT NOT NULL,
    imdb_id INTEGER,
    tmdb_id INTEGER,
    description TEXT,
    release_date TEXT,
    poster_path TEXT
);

CREATE TABLE user_watchlist (
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (movie_id) REFERENCES movie (id),
    PRIMARY KEY (user_id, movie_id)
);

CREATE TABLE user_watched (
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (movie_id) REFERENCES movie (id),
    PRIMARY KEY (user_id, movie_id)
);

CREATE TABLE genre (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE user_ratings (
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    rating INTEGER CHECK(rating BETWEEN 1 AND 5),
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (movie_id) REFERENCES movie (id),
    PRIMARY KEY (user_id, movie_id)
);

CREATE TABLE user_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    review TEXT,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (movie_id) REFERENCES movie (id)
);

