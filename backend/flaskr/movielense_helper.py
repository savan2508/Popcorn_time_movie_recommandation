import os
from datetime import datetime

import pandas as pd
from flask_smorest import Blueprint as ApiBlueprint
from flaskr import db, pin_required
from marshmallow import Schema, fields

from flaskr.database_models import MovielensMovie, MovielensRating

movielense_helper_blueprint = ApiBlueprint('movielense_helper', 'movielense_helper', url_prefix='/movielense_helper')

# Construct the absolute path
base_dir = os.path.abspath(os.path.dirname(__file__))
# base file path for machine learning models
base_path = os.path.join(base_dir, '../../machine_learning/')

# Load data
links = pd.read_csv(base_path + 'data/raw/ml-25m/links.csv')
movies_ml_25m = pd.read_csv(base_path + 'data/raw/ml-25m/movies.csv')
ratings_ml_25m_path = (base_path + 'data/raw/ml-25m/ratings.csv')

# Define the batch size for processing ratings data
BATCH_SIZE = 100000


# Define your schema for headers
class HeaderSchema(Schema):
    pin = fields.String(required=True)


@movielense_helper_blueprint.route('/populate_tables', methods=['POST'])
@movielense_helper_blueprint.arguments(schema=HeaderSchema)
@pin_required
def populate_tables(movies=movies_ml_25m, ratings=ratings_ml_25m_path, links=links):
    """
    Populate the tables with movie and rating data.

    ---
    tags:
      - Movielense Helper
    parameters:
      - pin: "string"
    responses:
      200:
        description: Tables populated successfully.
      401:
        description: Unauthorized. Invalid or missing PIN.
    """
    # Load CSV data
    movies_df = movies_ml_25m
    ratings_path = ratings
    links_df = links

    # Merge movies with links on movieId
    movies_with_links_df = movies_df.merge(links_df, on='movieId', how='left')

    # Check if tables are empty before inserting data
    if MovielensMovie.query.count() == 0:
        # Prepare movie data
        movie_data = movies_with_links_df[['movieId', 'title', 'genres', 'tmdbId', 'imdbId']].rename(columns={
            'movieId': 'movie_id',
            'title': 'movie_name',
            'tmdbId': 'tmdb_id',
            'imdbId': 'imdb_id'
        })

        # Insert movies into the database
        db.session.bulk_insert_mappings(MovielensMovie, movie_data.to_dict(orient='records'))
        db.session.commit()

    if MovielensRating.query.count() == 0:
        # Process ratings data in chunks
        for chunk in pd.read_csv(ratings_path, chunksize=BATCH_SIZE):
            # Convert the timestamp to datetime
            chunk['timestamp'] = chunk['timestamp'].apply(lambda x: datetime.fromtimestamp(x))
            # Prepare the chunk of ratings data
            rating_data_chunk = chunk.rename(columns={
                'movieId': 'movie_id',
                'userId': 'movielens_user_id'
            })

            # Insert the chunk of ratings into the database
            db.session.bulk_insert_mappings(MovielensRating, rating_data_chunk.to_dict(orient='records'))
            db.session.commit()

    return {'message': 'Tables populated successfully.'}