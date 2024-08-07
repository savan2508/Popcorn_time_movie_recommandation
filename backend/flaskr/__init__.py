import os
from datetime import timedelta

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_admin import Admin
from flask_smorest import Api
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
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'flaskr.sqlite')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY'),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1),
        API_TITLE='Popcorn Time API',
        API_VERSION='v1',
        OPENAPI_VERSION='3.0.3',
        OPENAPI_URL_PREFIX='/',
        OPENAPI_SWAGGER_UI_PATH='/swagger-ui/',
        OPENAPI_SWAGGER_UI_URL='https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
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
    db.init_app(app)
    migrate = Migrate(app, db)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Set up Flask-admin
    admin = Admin(app, name='Admin Interface', template_mode='bootstrap3', base_template='admin_master.html')
    from .database_models import User, Movie
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Movie, db.session))

    # Set up Flask-restful
    api = Api(app)

    # Register blueprints
    # from flaskr.models.genre_model import genre_blueprint
    # api.register_blueprint(genre_blueprint)

    # from flaskr.models.content_based_filtering import recommendation_blueprint
    # api.register_blueprint(recommendation_blueprint)

    from flaskr.models.auth import auth_blueprint
    api.register_blueprint(auth_blueprint)

    from .routes.user import user_blueprint
    api.register_blueprint(user_blueprint)

    return app
