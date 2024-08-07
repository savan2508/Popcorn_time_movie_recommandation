from flask import Blueprint, request, jsonify
from flaskr import database as db
from flaskr.database_models import User
from flaskr.schema import UserSchema
from marshmallow.exceptions import ValidationError

user_blueprint = Blueprint('users', 'users', url_prefix='/users')

# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_blueprint.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users))

@user_blueprint.route('/users', methods=['POST'])
def add_user():
    try:
        user_data = request.get_json()
        user = user_schema.load(user_data, session=db.session)
        db.session.add(user)
        db.session.commit()
        return user_schema.jsonify(user), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@user_blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return user_schema.jsonify(user)
