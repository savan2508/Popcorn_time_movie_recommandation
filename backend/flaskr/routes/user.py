from flask import Blueprint, request, jsonify
from flask_smorest import Blueprint as ApiBlueprint
from flaskr import database as db
from flaskr.database_models import User
from flaskr.schema import UserSchema
from marshmallow.exceptions import ValidationError

user_blueprint = ApiBlueprint('users', 'users', url_prefix='/users')

