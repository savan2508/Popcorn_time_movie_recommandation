from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flaskr.database import get_db
from flaskr import bcrypt

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user and bcrypt.check_password_hash(user['password_hash'], password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Bad username or password"}), 401
