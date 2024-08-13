import json
import os
import redis
import requests
from dotenv import load_dotenv

import numpy as np
import pandas as pd

from flaskr import db
from flaskr.database_models import MovielensMovie

# Load environment variables from the .env file
load_dotenv()

OMDB_API_KEY = os.getenv('OMDB_API_KEY')
OMDB_API_URL = "https://www.omdbapi.com/"

# Set up Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def format_imdb_id(imdb_id):
    """
    Format the IMDb ID to the OMDB API required format.

    Args:
        imdb_id (int): The integer IMDb ID.

    Returns:
        str: The formatted IMDb ID, e.g., "tt1234567".
    """
    return f"tt{str(imdb_id).zfill(7)}"


def fetch_omdb_details(imdb_id):
    """
    Fetch movie details from OMDB API and cache the result.

    Args:
        imdb_id (str): The formatted IMDb ID.

    Returns:
        dict: The movie details from OMDB API, or None if an error occurs.
    """
    # Check Redis cache
    cached_data = redis_client.get(imdb_id)
    if cached_data:
        print(f"Cache hit for {imdb_id}")
        return json.loads(cached_data)

    print(f"Cache miss for {imdb_id}. Fetching from OMDB API.")

    params = {
        'i': imdb_id,
        'apikey': OMDB_API_KEY,
        'plot': 'full',
    }

    try:
        response = requests.get(OMDB_API_URL, params=params)
        response.raise_for_status()
        movie_details = response.json()

        if movie_details.get('Response') == 'True':
            # Store in Redis cache with an expiration time (e.g., 1 day)
            redis_client.setex(imdb_id, 86400, json.dumps(movie_details))
            return movie_details
        else:
            print(f"Error fetching details for IMDb ID {imdb_id}: {movie_details.get('Error')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None


def get_movie_details(movies):
    """
    Get detailed information for a list of movies.
    :param movies:
    :return:
    """
    if type(movies) != list:
        movies = [movies]
    else:
        # Retrieve movie names in a single query
        movies = [movie.movie_id for movie in movies]

    movie_details_list = []

    for movie in movies:
        # Basic movie details
        movie_details = {
            "movie_id": movie,
            "movie_name": MovielensMovie.query.get(movie).movie_name,
            "genres": MovielensMovie.query.get(movie).genres,
            "imdb_id": MovielensMovie.query.get(movie).imdb_id,
            "tmdb_id": MovielensMovie.query.get(movie).tmdb_id
        }

        # Fetch additional details from OMDB
        if movie_details['imdb_id']:
            omdb_details = fetch_omdb_details(format_imdb_id(movie_details['imdb_id']))
            if omdb_details:
                movie_details.update({
                    "omdb_title": omdb_details.get('Title'),
                    "omdb_year": omdb_details.get('Year'),
                    "omdb_director": omdb_details.get('Director'),
                    "omdb_actors": omdb_details.get('Actors'),
                    "omdb_plot": omdb_details.get('Plot'),
                    "omdb_poster": omdb_details.get('Poster'),
                    "omdb_rating": omdb_details.get('imdbRating'),
                    "omdb_genres": omdb_details.get('Genre')
                })

        # Conditionally add avg_rating and rating_count if they exist
        if hasattr(movie, 'avg_rating'):
            movie_details["avg_rating"] = movie.avg_rating

        if hasattr(movie, 'rating_count'):
            movie_details["rating_count"] = movie.rating_count

        movie_details_list.append(movie_details)

    return movie_details_list


def age_map_convertor(age):
    if age <= 18:
        return 1
    elif age <= 24:
        return 18
    elif age <= 34:
        return 25
    elif age <= 44:
        return 35
    elif age <= 49:
        return 45
    elif age <= 55:
        return 50
    else:
        return 56


def prepare_data(age, occupation, gender, age_encoder, occupation_encoder, age_map):
    possible_gender_values_map = {
        "male": 1,
        "female": 0,
        "1": 1,
        "0": 0,
        1: 1,
        0: 0,
    }
    gender = possible_gender_values_map[gender]

    age_str = age_map[age_map_convertor(age)]
    age_input = np.array(age_str).reshape(1, -1)
    occupation_input = np.array(occupation).reshape(1, -1)

    age_encoded = age_encoder.transform(age_input).toarray()
    occupation_encoded = occupation_encoder.transform(occupation_input).toarray()

    input_features = np.hstack([gender, age_encoded.flatten(), occupation_encoded.flatten()])
    input_features = input_features.reshape(1, -1)

    feature_names = ['gender'] + list(age_encoder.get_feature_names_out(['AgeRange'])) + list(
        occupation_encoder.get_feature_names_out(['Occupation']))
    input_features_df = pd.DataFrame(input_features, columns=feature_names)

    return input_features_df
