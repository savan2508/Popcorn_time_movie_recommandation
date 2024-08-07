from flask import Blueprint, request, jsonify, make_response
from flask_smorest import Blueprint as ApiBlueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr import db
from flaskr.database_models import User
from flaskr.schema import UserSchema, UserSignInSchema, UserSignupSchema

auth_blueprint = ApiBlueprint('auth', 'auth', url_prefix='/auth', description='Authentication endpoints')

# Define schemas
user_signin_schema = UserSignInSchema()
user_signup_schema = UserSignupSchema()


@auth_blueprint.route('/signup', methods=['POST'])
@auth_blueprint.arguments(user_signup_schema)
# @auth_blueprint.response(201, UserSchema)
def signup(user_data):
    """Register a new user

        This endpoint registers a new user. It expects the following fields:
        - first_name (required): The first name of the user.
        - last_name (required): The last name of the user.
        - age (optional): The age of the user, must be a non-negative integer.
        - gender (required): The gender of the user, must be one of 'male' or 'female'.
        - occupation (optional): The occupation of the user.
        - preferred_genre (optional): The preferred genre of the user.
        - email (required): The email address of the user.
        - username (required): The username for the user account.
        - password (required): The password for the user account, minimum 8 characters.

        Returns a JSON object of the newly created user.
        """
    existing_user_email = User.query.filter_by(email=user_data['email']).first()
    if existing_user_email:
        abort(409, message="User already exists with that email.")
    existing_user_username = User.query.filter_by(username=user_data['username']).first()
    if existing_user_username:
        abort(409, message="User already exists with that username.")
    password = user_data.pop('password')
    user = User(**user_data)
    user.password_hash = generate_password_hash(password)
    db.session.add(user)
    db.session.commit()
    return "User created", 201


@auth_blueprint.route('/signin', methods=['POST'])
@auth_blueprint.arguments(user_signin_schema)
def signin(credentials):
    user = User.query.filter_by(email=credentials['email']).first()
    if user and check_password_hash(user.password_hash, credentials['password']):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        response = make_response(jsonify(message="Login successful"))
        response.set_cookie('access_token_cookie', access_token, httponly=True, samesite='Strict', secure=True)
        response.set_cookie('refresh_token_cookie', refresh_token, httponly=True, samesite='Strict', secure=True)
        return response
    else:
        abort(401, message="Invalid credentials.")


@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token)


@auth_blueprint.route('/sign_out', methods=['POST'])
def sign_out():
    response = make_response(jsonify(message="Logout successful"))
    response.delete_cookie('access_token_cookie')
    response.delete_cookie('refresh_token_cookie')
    return response
