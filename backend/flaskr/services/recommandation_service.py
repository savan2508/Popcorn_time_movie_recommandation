import os

import numpy as np
import joblib

from scipy.sparse import csr_matrix
from flaskr.services.data_preparation import get_movie_details

from flaskr.database_models import MovielensMovie

# Construct the absolute path
base_dir = os.path.abspath(os.path.dirname(__file__))
# base file path for machine learning models
base_path = os.path.join(base_dir, '../../../machine_learning/models/')
# Load the similarity matrix
sparse_similarity_matrix = csr_matrix(joblib.load(base_path + 'cosine_similarity_matrix.joblib', mmap_mode='r'))


def get_recommendations(movie_id, movie_indices, top_n=10):
    index_to_movie_id = {v: k for k, v in movie_indices.items()}

    idx = movie_indices.get(movie_id)
    if idx is None:
        return []

    sim_scores = sparse_similarity_matrix[idx].toarray().flatten()
    sorted_indices = np.argsort(sim_scores)[::-1]

    top_similar_indices = [index_to_movie_id[j] for j in sorted_indices[:top_n] if j != idx]
    return top_similar_indices


def find_movie_ids_by_name(movie_name):
    matching_movies = MovielensMovie.query.filter(
        MovielensMovie.movie_name.ilike(f"%{movie_name}%")
    ).all()
    return [movie.movie_id for movie in matching_movies]


def get_movie_ids(movie_input):
    movie_ids = []
    if isinstance(movie_input, list):
        for movie in movie_input:
            if isinstance(movie, int):
                movie_ids.append(movie)
            elif isinstance(movie, str):
                movie_ids.extend(find_movie_ids_by_name(movie))
            else:
                return "Invalid input type. Please provide a movie ID (int) or movie name (str)."
    elif isinstance(movie_input, int) or isinstance(movie_input, str):
        if isinstance(movie_input, int):
            movie_ids = [movie_input]
        elif isinstance(movie_input, str):
            movie_ids = find_movie_ids_by_name(movie_input)
            if not movie_ids:
                return f"No movie with the name '{movie_input}' exists. Please try again."
    else:
        return "Invalid input type. Please provide a movie ID (int), movie name (str) or list of movie IDs/names."

    return movie_ids


def get_movie_recommendations(movie_input, top_n=10):
    top_n = top_n + 1 # Include the input movie in the recommendations
    input_movie_ids = get_movie_ids(movie_input)
    # movie_indices_local = {movieId: idx for idx, movieId in enumerate(movie_dataset['movieId'])}
    movie_indices_local = {
        movie.movie_id: idx for idx, movie in enumerate(MovielensMovie.query.all())
    }
    recommendations_dict = []

    for movie_id in input_movie_ids:
        movie = MovielensMovie.query.get(movie_id)
        if not movie:
            continue

        input_movie_info = get_movie_details(movie_id)[0]

        # Get the recommendations based on the movie ID
        _recommendations = get_recommendations(movie_id, movie_indices=movie_indices_local, top_n=top_n)
        print(f"Recommendations for movie ID {movie_id}: {_recommendations}")

        recommended_movies_info = []

        for rec_movie_id in _recommendations:
            recommended_movie = get_movie_details(rec_movie_id)[0]
            if recommended_movie:
                movie_info = recommended_movie
                recommended_movies_info.append(movie_info)

        recommendations_dict.append({
            'movie': input_movie_info,
            'recommended_movies': recommended_movies_info
        })

    return recommendations_dict
