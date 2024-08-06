import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from dotenv import load_dotenv

load_dotenv()
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()


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
        database.init_app(app)
    migrate = Migrate(app, db)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Set up Flask-admin
    admin = Admin(app, name='Admin Interface', template_mode='bootstrap3')
    from .models import User, Movie
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Movie, db.session))

    # Register blueprints
    from .models.genre_model import genre_blueprint
    from .models.content_based_filtering import recommendation_blueprint
    from .models.auth import auth_blueprint
    app.register_blueprint(genre_blueprint)
    app.register_blueprint(recommendation_blueprint)
    app.register_blueprint(auth_blueprint)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, from Popcorn_time API!'

    return app
