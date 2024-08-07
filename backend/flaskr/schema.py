from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from .database_models import *


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_relationships = True


class MovieSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Movie
        load_instance = True
        include_relationships = True


class GenreSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Genre
        load_instance = True

class UserWatchlistSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserWatchlist
        load_instance = True
    user = Nested(UserSchema, only=['id', 'username'])
    movie = Nested(MovieSchema, only=['id', 'title'])


class UserWatchedSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserWatched
        load_instance = True
    user = Nested(UserSchema, only=['id', 'username'])
    movie = Nested(MovieSchema, only=['id', 'title'])


class UserRatingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserRatings
        load_instance = True
    user = Nested(UserSchema, only=['id', 'username'])
    movie = Nested(MovieSchema, only=['id', 'title'])


class UserReviewSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserReviews
        load_instance = True
    user = Nested(UserSchema, only=['id', 'username'])
    movie = Nested(MovieSchema, only=['id', 'title'])
