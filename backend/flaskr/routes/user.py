from flask import jsonify, request
from flask_smorest import Blueprint as ApiBlueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask.views import MethodView

from flaskr import db
from flaskr.database_models import User, UserWatchlist, UserWatchHistory, UserReviews, UserRatings
from flaskr.decorators import swagger_doc
from flaskr.schema import UserInfoSchema, UserWatchlistSchema, UserRatingSchema, UserWatchHistorySchema, \
    UserReviewSchema
import logging
from flaskr.services.data_preparation import get_movie_details

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

user_info_blueprint = ApiBlueprint('user_info', __name__, url_prefix='/user')
user_actions_blueprint = ApiBlueprint('user_actions', 'user_actions', url_prefix='/user_actions')

# Define the user information schema for documentation
user_schema = UserInfoSchema()


@user_info_blueprint.route('/info', methods=['GET'])
class UserInfoResource(MethodView):  # Inherit from MethodView
    @jwt_required()
    @user_info_blueprint.doc(security=[{'bearerAuth': []}])
    def get(self):
        """
        Retrieve user information.

        This endpoint retrieves information about the authenticated user.

        ---
        security:
          - bearerAuth: []
        responses:
          200:
            description: A user object
            content:
              application/json:
                schema: UserInfoSchema
          404:
            description: User not found
        """
        # Get the identity of the current user
        current_user_id = get_jwt_identity()
        logger.debug("current_user_id: %s", current_user_id)

        # Query the database for the user
        user = User.query.filter_by(id=current_user_id).first()
        logger.debug("user: %s", user)

        # If the user is not found, return a 404 response
        if user is None:
            return jsonify(message='User not found'), 404

        # Serialize the user object
        user_data = user_schema.dump(user)
        logger.debug("user: %s", user_data)

        return user_data, 200


@user_actions_blueprint.route('/watchlist', methods=['GET', 'POST'])
@user_actions_blueprint.doc(
    description="Manage user's watchlist.",
    parameters=[
        {
            "name": "Authorization",
            "in": "header",
            "required": True,
            "schema": {"type": "string"},
            "description": "JWT token to authorize the request"
        },
        {
            "name": "movie_id",
            "in": "body",
            "required": False,
            "description": "Movie ID to add to the watchlist (required for POST)"
        }
    ],
    requestBody={
        "required": False,
        "headers": {
            "Authorization": {
                "description": "JWT",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "string"
                        }
                    }
                }
            }
        },
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "movie_id": {
                            "type": "integer",
                            "description": "Movie ID to add to the watchlist (required for POST)"
                        }
                    },
                }
            }
        }
    },
    responses={
        200: {"description": "Successfully retrieved or modified watchlist"},
        400: {"description": "Bad request or movie already exists in watchlist"},
        401: {"description": "Unauthorized access"}
    }
)
@jwt_required()
def manage_watchlist():
    user_id = get_jwt_identity()

    if request.method == 'GET':
        # Retrieve user's watchlist
        watchlist = UserWatchlist.query.filter_by(user_id=user_id).all()
        movie_list = get_movie_details(watchlist)
        return jsonify(movie_list)

    if request.method == 'POST':
        # Add a movie to the user's watchlist
        data = request.get_json()
        movie_id = data.get('movie_id')
        if not movie_id:
            return jsonify({"message": "Movie ID is required"}), 400

        # Check if the movie is already in the watchlist
        existing_entry = UserWatchlist.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if existing_entry:
            return jsonify({"message": "Movie already in watchlist"}), 400

        watchlist_entry = UserWatchlist(user_id=user_id, movie_id=movie_id)
        db.session.add(watchlist_entry)
        db.session.commit()
        return jsonify({"message": "Movie added to watchlist"}), 201


@user_actions_blueprint.delete('/watchlist')
@jwt_required()
@user_actions_blueprint.doc(
    description="Delete a movie from the user's watchlist.",
    parameters=[
        {
            "name": "Authorization",
            "in": "header",
            "required": True,
            "schema": {"type": "string"},
            "description": "JWT token to authorize the request"
        },
        {
            "name": "movie_id",
            "in": "body",
            "required": False,
            "description": "Movie ID to add to the watchlist (required for POST)"
        }
    ],
    responses={
        200: {"description": "Successfully removed movie from watchlist"},
        404: {"description": "Bad request or movie doesn't exists in watchlist"},
        401: {"description": "Unauthorized access"}
    }
)
def delete_from_watchlist():
    data = request.get_json()
    movie_id = data.get('movie_id')
    user_id = get_jwt_identity()

    watchlist_entry = UserWatchlist.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if not watchlist_entry:
        return jsonify({"message": "Movie not found in watchlist"}), 404

    db.session.delete(watchlist_entry)
    db.session.commit()
    return jsonify({"message": "Movie removed from watchlist"}), 200


@user_actions_blueprint.route('/ratings', methods=['GET', 'POST', 'PUT'])
@jwt_required()
@user_actions_blueprint.doc(
    description="Manage user's ratings.",
    parameters=[
        {
            "name": "Authorization",
            "in": "header",
            "required": True,
            "schema": {"type": "string"},
            "description": "JWT token to authorize the request"
        },
        {
            "name": "movie_id",
            "in": "body",
            "required": False,
            "description": "Movie ID to add to the watchlist (required for POST)"
        },
        {
            "name": "rating",
            "in": "body",
            "required": False,
            "schema": {"type": "integer"},
            "description": "Rating value (required for POST)"
        }
    ],
    responses={
        200: {"description": "Successfully retrieved or modified ratings"},
        201: {"description": "Rating added/updated"},
        400: {"description": "Bad request or movie doesn't exists in watchlist"},
        401: {"description": "Unauthorized access"}
    }
)
def manage_ratings():
    user_id = get_jwt_identity()

    if request.method == 'GET':
        # Retrieve user's ratings
        ratings = UserRatings.query.filter_by(user_id=user_id).all()
        schema = UserRatingSchema(many=True)
        return jsonify(schema.dump(ratings))

    if request.method == 'POST':
        # Add or update a rating
        data = request.get_json()
        movie_id = data.get('movie_id')
        rating_value = data.get('rating')

        rating_entry = UserRatings.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if rating_entry:
            # Update existing rating
            rating_entry.rating = rating_value
        else:
            # Add new rating
            rating_entry = UserRatings(user_id=user_id, movie_id=movie_id, rating=rating_value)
            db.session.add(rating_entry)

        db.session.commit()
        return jsonify({"message": "Rating added/updated"}), 201

    if request.method == 'PUT':
        # Update an existing rating
        data = request.get_json()
        movie_id = data.get('movie_id')
        rating_value = data.get('rating')

        rating_entry = UserRatings.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if not rating_entry:
            return jsonify({"message": "Rating not found"}), 404

        rating_entry.rating = rating_value
        db.session.commit()
        return jsonify({"message": "Rating updated"}), 200


@user_actions_blueprint.route('/ratings/<int:movie_id>', methods=['DELETE'])
@jwt_required()
def delete_rating(movie_id):
    user_id = get_jwt_identity()

    rating_entry = UserRatings.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if not rating_entry:
        return jsonify({"message": "Rating not found"}), 404

    db.session.delete(rating_entry)
    db.session.commit()
    return jsonify({"message": "Rating deleted"}), 200


@user_actions_blueprint.route('/reviews', methods=['GET', 'POST', 'PUT'])
@jwt_required()
def manage_reviews():
    user_id = get_jwt_identity()

    if request.method == 'GET':
        # Retrieve user's reviews
        reviews = UserReviews.query.filter_by(user_id=user_id).all()
        schema = UserReviewSchema(many=True)
        return jsonify(schema.dump(reviews))

    if request.method == 'POST':
        # Add or update a review
        data = request.get_json()
        movie_id = data.get('movie_id')
        review_text = data.get('review')

        review_entry = UserReviews.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if review_entry:
            # Update existing review
            review_entry.review = review_text
        else:
            # Add new review
            review_entry = UserReviews(user_id=user_id, movie_id=movie_id, review=review_text)
            db.session.add(review_entry)

        db.session.commit()
        return jsonify({"message": "Review added/updated"}), 201

    if request.method == 'PUT':
        # Update an existing review
        data = request.get_json()
        movie_id = data.get('movie_id')
        review_text = data.get('review')

        review_entry = UserReviews.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if not review_entry:
            return jsonify({"message": "Review not found"}), 404

        review_entry.review = review_text
        db.session.commit()
        return jsonify({"message": "Review updated"}), 200


@user_actions_blueprint.route('/reviews/<int:movie_id>', methods=['DELETE'])
@jwt_required()
def delete_review(movie_id):
    user_id = get_jwt_identity()

    review_entry = UserReviews.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if not review_entry:
        return jsonify({"message": "Review not found"}), 404

    db.session.delete(review_entry)
    db.session.commit()
    return jsonify({"message": "Review deleted"}), 200


@user_actions_blueprint.route('/watch_history', methods=['GET', 'POST'])
@jwt_required()
def manage_watch_history():
    user_id = get_jwt_identity()

    if request.method == 'GET':
        # Retrieve user's watch history
        watch_history = UserWatchHistory.query.filter_by(user_id=user_id).all()
        movies = get_movie_details(watch_history)
        return jsonify(movies)

    if request.method == 'POST':
        # Add a movie to the user's watch history
        data = request.get_json()
        movie_id = data.get('movie_id')

        # Check if the movie is already marked as watched
        existing_entry = UserWatchHistory.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if existing_entry:
            return jsonify({"message": "Movie already marked as watched"}), 400

        watch_history_entry = UserWatchHistory(user_id=user_id, movie_id=movie_id)
        db.session.add(watch_history_entry)
        db.session.commit()
        return jsonify({"message": "Movie marked as watched"}), 201


@user_actions_blueprint.route('/watch_history/<int:movie_id>', methods=['DELETE'])
@jwt_required()
def delete_from_watch_history(movie_id):
    user_id = get_jwt_identity()

    watch_history_entry = UserWatchHistory.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if not watch_history_entry:
        return jsonify({"message": "Movie not found in watch history"}), 404

    db.session.delete(watch_history_entry)
    db.session.commit()
    return jsonify({"message": "Movie removed from watch history"}), 200
