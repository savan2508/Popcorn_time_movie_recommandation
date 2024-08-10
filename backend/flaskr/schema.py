from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, Schema, validate, validates, ValidationError
from marshmallow_sqlalchemy.fields import Nested
from .database_models import *


class UserInfoSchema(Schema):
    first_name = fields.String()
    last_name = fields.String()
    age = fields.Integer()
    gender = fields.String()
    occupation = fields.String()
    preferred_genre = fields.String()
    recommended_genre = fields.String()
    email = fields.Email()
    username = fields.String()
    id = fields.Integer()


class UserSignInSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))


class UserSignupSchema(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(min=1))
    last_name = fields.Str(required=True, validate=validate.Length(min=1))
    age = fields.Int(required=False, validate=validate.Range(min=0))
    gender = fields.Str(required=True, validate=validate.OneOf(["male", "female"]))
    occupation = fields.Str(required=False)
    preferred_genre = fields.Str(required=False)
    # recommended_genre = fields.Str(required=False)
    email = fields.Email(required=True)
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=8))

    @validates('age')
    def validate_age(self, value):
        if value is not None and value < 0:
            raise ValidationError("Age must be a non-negative integer.")


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

    user = Nested(UserInfoSchema, only=['id', 'username'])
    movie = Nested(MovieSchema, only=['id', 'title'])


class UserWatchedSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserWatched
        load_instance = True

    user = Nested(UserInfoSchema, only=['id', 'username'])
    movie = Nested(MovieSchema, only=['id', 'title'])


class UserRatingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserRatings
        load_instance = True

    user = Nested(UserInfoSchema, only=['id', 'username'])
    movie = Nested(MovieSchema, only=['id', 'title'])


class UserReviewSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserReviews
        load_instance = True

    user = Nested(UserInfoSchema, only=['id', 'username'])
    movie = Nested(MovieSchema, only=['id', 'title'])
