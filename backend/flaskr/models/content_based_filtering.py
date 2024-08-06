from flask import Blueprint, request, jsonify
import pandas as pd
from flaskr.services.recommandation_service import get_movie_recommendations

recommendation_blueprint = Blueprint('recommendation', __name__)

# Load data
links = pd.read_csv('../data/raw/ml-25m/links.csv')
movies_ml_25m = pd.read_csv('../data/raw/ml-25m/movies.csv')

@recommendation_blueprint.route('/recommend_movies', methods=['POST'])
def recommend_movies():
    data = request.json
    movie_input = data.get('movie_input')
    top_n = data.get('top_n', 10)

    recommendations_dict = get_movie_recommendations(movie_input, top_n, movies_ml_25m, links)

    return jsonify(recommendations_dict)
