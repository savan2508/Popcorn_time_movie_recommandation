import os
from datetime import timedelta
import random
from functools import wraps
import subprocess
import time
import redis

from flask import Flask, jsonify, request, current_app
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_admin import Admin
from flask_smorest import Api
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS
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
        DEBUG=True,
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

    # Start Redis when the Flask app starts
    start_redis()

    # Set up Redis client
    try:
        redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
        redis_client.ping()  # Test connection
        # Attach the Redis client to the app context
        app.redis_client = redis_client
        print("Connected to Redis")
    except redis.exceptions.ConnectionError as e:
        print(f"Redis connection error: {e}")

    # Configure CORS
    cors = CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    # Set up Flask-admin
    admin = Admin(app, name='Admin Interface', template_mode='bootstrap3')
    from flaskr.database_models import User, Movie, MovielensMovie
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Movie, db.session))
    admin.add_view(ModelView(MovielensMovie, db.session))

    # Set up Flask-restful
    api = Api(app, )

    # Define the bearerAuth security scheme
    api.spec.components.security_scheme("bearerAuth", {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    })

    # Register the schema with the API
    from .schema import UserInfoSchema, UserSignupSchema, UserSignInSchema
    # Register schemas with unique names
    api.spec.components.schema('UserInfo', schema=UserInfoSchema)
    api.spec.components.schema('UserSignup', schema=UserSignupSchema)
    api.spec.components.schema('UserSignIn', schema=UserSignInSchema)

    from flaskr.models.auth import auth_blueprint
    api.register_blueprint(auth_blueprint)

    from flaskr.routes.user import user_info_blueprint
    api.register_blueprint(user_info_blueprint)

    from flaskr.routes.user import user_actions_blueprint
    api.register_blueprint(user_actions_blueprint)

    from flaskr.models.movie_recommendations import movies_recommendation_blueprint
    api.register_blueprint(movies_recommendation_blueprint)

    from flaskr.movielense_helper import movielense_helper_blueprint
    api.register_blueprint(movielense_helper_blueprint)

    # Generate and store the PIN
    app.config['POPULATE_TABLES_PIN'] = generate_pin()
    print(f"Generated PIN: {app.config['POPULATE_TABLES_PIN']}")

    return app


def pin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Parse JSON data from the request body
        json_data = request.get_json()

        # Extract the 'pin' from the JSON data
        pin = json_data.get('pin') if json_data else None
        print(f"PIN from JSON body: {pin}")

        # Compare the extracted PIN with the expected PIN
        if pin != current_app.config['POPULATE_TABLES_PIN']:
            return jsonify({"message": "Unauthorized"}), 401

        return f(*args, **kwargs)

    return decorated_function


def generate_pin():
    return str(random.randint(1000, 9999))


def start_redis():
    """
    Start the Redis server as a subprocess.
    """
    try:
        subprocess.Popen(['redis-server'])  # Start Redis server as a subprocess
        time.sleep(1)  # Wait for Redis to start
        print("Redis server started successfully.")
    except Exception as e:
        print(f"Error starting Redis server: {e}")
