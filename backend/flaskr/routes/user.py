from flask import request, jsonify
from flask_smorest import Blueprint as ApiBlueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flaskr import database as db
from flaskr.database_models import User
from flaskr.schema import UserSchema
from marshmallow.exceptions import ValidationError

user_blueprint = ApiBlueprint('users', 'users', url_prefix='/users')

# Define the user information schema for documentation
user_schema = UserSchema()


@user_blueprint.route('/info', methods=['POST'])
@user_blueprint.response(200, UserSchema)
@user_blueprint.response(404, 'User not found')
@jwt_required()
def get_user_info():
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
                schema: UserSchema
          404:
            description: User not found
    """
    # Get the identity of the current user
    current_user_email = get_jwt_identity()

    # Query the database for the user
    user = User.query.filter_by(email=current_user_email).first()

    # If the user is not found, return a 404 response
    if user is None:
        return jsonify(message='User not found'), 404

    # Serialize the user object
    user_data = user_schema.dump(user)

    return user_data, 200
