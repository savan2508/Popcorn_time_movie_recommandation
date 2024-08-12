import os

from flask import Blueprint, request, jsonify
import pandas as pd
from flaskr.services.recommandation_service import get_movie_recommendations

recommendation_blueprint = Blueprint('recommendation', __name__)

# Construct the absolute path
# base_dir = os.path.abspath(os.path.dirname(__file__))
# base file path for machine learning models
# base_path = os.path.join(base_dir, '../../../machine_learning/')

# Load data
# links = pd.read_csv(base_path + 'data/raw/ml-25m/links.csv')
# movies_ml_25m = pd.read_csv(base_path + 'data/raw/ml-25m/movies.csv')


@recommendation_blueprint.route('/recommend_movies', methods=['POST'])
def recommend_movies():
    data = request.json
    movie_input = data.get('movie_input')
    top_n = data.get('top_n', 10)

    recommendations_dict = get_movie_recommendations(movie_input, top_n)

    return jsonify(recommendations_dict)
