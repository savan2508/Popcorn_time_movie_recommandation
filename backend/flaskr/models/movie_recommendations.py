from wsgiref import validate

from flask_smorest import Blueprint as ApiBlueprint
from flaskr import db
from flaskr.database_models import MovielensMovie, MovielensRating
from sqlalchemy import func
from flask import request, jsonify
from marshmallow import Schema, fields

from flaskr.services.data_preparation import get_movie_details
from flaskr.services.recommandation_service import get_movie_recommendations

movies_recommendation_blueprint = ApiBlueprint('movies_recommendation', 'movies_recommendation',
                                               url_prefix='/movies_recommendation',
                                               description='Movie recommendation endpoints')


class MovieRecommendationSchema(Schema):
    movie_input = fields.Raw(
        description="A movie ID, movie name, or a list of movie IDs/names.",
    )
    top_n = fields.Integer(
        description="The number of top recommendations to return.",
        default=10,
    )


@movies_recommendation_blueprint.route('/recommend_movies', methods=['POST'])
@movies_recommendation_blueprint.arguments(MovieRecommendationSchema)
def recommend_movies(data):
    """
    Recommend movies based on the input movie(s).

    ---
    - tags:
      - Movies Recommendation
    - requestBody:
      - required: true
      - content:
         - application/json:
          - schema:
            - type: object
            - properties:
              - movie_input:
                - type: [string, integer, array]
                - description: A movie ID, movie name, or a list of movie IDs/names.
              - top_n:
                - type: integer
                - description: The number of top recommendations to return.
                - default: 10
    responses:
      -200:
        description: A list of recommended movies.
        content:
          application/json:
            schema:
              type: object
              properties:
                movie_id:
                  type: integer
                  description: The ID of the input movie.
                movie_name:
                  type: string
                  description: The name of the input movie.
                recommended_movies:
                  type: array
                  items:
                    type: object
                    properties:
                      movie_id:
                        type: integer
                        description: The ID of the recommended movie.
                      movie_name:
                        type: string
                        description: The name of the recommended movie.
                      genres:
                        type: string
                        description: The genres of the recommended movie.
                      imdb_id:
                        type: string
                        description: The IMDb ID of the recommended movie.
                      tmdb_id:
                        type: string
                        description: The TMDb ID of the recommended movie.
      400:
        description: Invalid input.
    """
    # data = request.json
    movie_input = data.get('movie_input')
    top_n = data.get('top_n', 10)

    recommendations_dict = get_movie_recommendations(movie_input, top_n)

    return jsonify(recommendations_dict)


@movies_recommendation_blueprint.route('/<genre>/top_rated', methods=['GET'])
def get_top_movies(genre):
    """
    Get top 10 movies for a given genre by average rating and number of ratings.

    ---
    parameters:
      - name: genre
        in: path
        required: true
        schema:
          type: string
        description: The genre to filter movies by (case-insensitive).
    responses:
      200:
        description: A list of top movies in the specified genre.
      404:
        description: Genre not found.
    """
    genre = genre.lower()  # Normalize genre input to lowercase

    # Query movies of the specified genre
    movies_in_genre = MovielensMovie.query.filter(
        MovielensMovie.genres.ilike(f'%{genre}%')
    ).all()

    if not movies_in_genre:
        return jsonify({"message": "Genre not found"}), 404

    movie_ids = [movie.movie_id for movie in movies_in_genre]

    # Calculate average rating and count of ratings for each movie
    ratings_agg = (db.session.query(
        MovielensRating.movie_id,
        func.avg(MovielensRating.rating).label('avg_rating'),
        func.count(MovielensRating.rating).label('rating_count')
    ).filter(
        MovielensRating.movie_id.in_(movie_ids)
    ).group_by(
        MovielensRating.movie_id
    ).having(
        func.count(MovielensRating.rating) > 50
    ).all())

    # Sort by average rating and number of ratings
    top_rated_movies = sorted(ratings_agg, key=lambda x: x.avg_rating, reverse=True)[:10]
    most_rated_movies = sorted(ratings_agg, key=lambda x: x.rating_count, reverse=True)[:10]

    # Retrieve movie details
    top_rated_details = get_movie_details(top_rated_movies)
    most_rated_details = get_movie_details(most_rated_movies)

    return jsonify({
        "top_rated_movies": top_rated_details,
        "most_rated_movies": most_rated_details
    })


@movies_recommendation_blueprint.route('/popular', methods=['GET'])
def get_popular_movies():
    """
    Get top 50 movies by average rating and top 50 movies by the number of ratings across all genres.

    ---
    responses:
      200:
        description: A list of popular movies.
    """
    # Calculate average rating and count of ratings for each movie
    ratings_agg = db.session.query(
        MovielensRating.movie_id,
        func.avg(MovielensRating.rating).label('avg_rating'),
        func.count(MovielensRating.rating).label('rating_count')
    ).group_by(
        MovielensRating.movie_id
    ).all()

    # Sort by average rating and number of ratings
    top_rated_movies = sorted(ratings_agg, key=lambda x: x.avg_rating, reverse=True)[:50]
    most_rated_movies = sorted(ratings_agg, key=lambda x: x.rating_count, reverse=True)[:50]

    # Retrieve movie details
    top_rated_details = get_movie_details(top_rated_movies)
    most_rated_details = get_movie_details(most_rated_movies)

    return jsonify({
        "top_rated_movies": top_rated_details,
        "most_rated_movies": most_rated_details
    })
