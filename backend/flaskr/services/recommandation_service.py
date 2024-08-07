import os

import numpy as np
import pandas as pd
import joblib
from scipy.sparse import csr_matrix

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


def find_movie_ids_by_name(movie_name, movie_dataset):
    movie_name_lower = movie_name.lower()
    matching_movies = movie_dataset[movie_dataset['title'].str.lower().str.contains(movie_name_lower)]
    return matching_movies['movieId'].tolist()


def get_movie_ids(movie_input, movie_dataset):
    movie_ids = []
    if isinstance(movie_input, list):
        for movie in movie_input:
            if isinstance(movie, int):
                movie_ids.append(movie)
            elif isinstance(movie, str):
                movie_ids.extend(find_movie_ids_by_name(movie, movie_dataset))
            else:
                return "Invalid input type. Please provide a movie ID (int) or movie name (str)."
    elif isinstance(movie_input, int) or isinstance(movie_input, str):
        if isinstance(movie_input, int):
            movie_ids = [movie_input]
        elif isinstance(movie_input, str):
            movie_ids = find_movie_ids_by_name(movie_input, movie_dataset)
            if not movie_ids:
                return f"No movie with the name '{movie_input}' exists. Please try again."
    else:
        return "Invalid input type. Please provide a movie ID (int), movie name (str) or list of movie IDs/names."

    return movie_ids


def get_movie_recommendations(movie_input, top_n, movie_dataset, link_dataset):
    movie_ids = get_movie_ids(movie_input, movie_dataset)
    movie_indices_local = {movieId: idx for idx, movieId in enumerate(movie_dataset['movieId'])}

    recommendations_dict = {}

    for movie_id in movie_ids:
        movie_name = movie_dataset[movie_dataset['movieId'] == movie_id]['title'].values[0]
        _recommendations = get_recommendations(movie_id, movie_indices=movie_indices_local, top_n=top_n)

        recommended_movies_info = []

        for rec_movie_id in _recommendations:
            recommended_movie = movie_dataset[movie_dataset['movieId'] == rec_movie_id]
            if not recommended_movie.empty:
                movie_info = {
                    'movie_name': recommended_movie['title'].values[0],
                    'genre': recommended_movie['genres'].values[0],
                    'movieId': rec_movie_id,
                    'imdb_id': link_dataset[link_dataset['movieId'] == rec_movie_id]['imdbId'].values[0],
                    'tmdb_id': link_dataset[link_dataset['movieId'] == rec_movie_id]['tmdbId'].values[0]
                }
                recommended_movies_info.append(movie_info)

        recommendations_dict[movie_id] = {
            'movie_name': movie_name,
            'recommended_movies': recommended_movies_info
        }

    return recommendations_dict
