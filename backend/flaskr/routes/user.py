from flask import jsonify
from flask_smorest import Blueprint as ApiBlueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask.views import MethodView
from flaskr.database_models import User
from flaskr.schema import UserInfoSchema
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

user_info_blueprint = ApiBlueprint('user_info', __name__, url_prefix='/user')

# Define the user information schema for documentation
user_schema = UserInfoSchema()


@user_info_blueprint.route('/info', methods=['GET'])
class UserInfoResource(MethodView):  # Inherit from MethodView
    @jwt_required()
    # @user_info_blueprint.response(200, UserInfoSchema)
    # @user_info_blueprint.response(404, 'User not found')
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
