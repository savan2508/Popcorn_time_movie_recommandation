import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Initialize the database, bcrypt and JWT
    bcrypt.init_app(app)
    jwt.init_app(app)
    with app.app_context():
        from . import database
        db.init_app(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
