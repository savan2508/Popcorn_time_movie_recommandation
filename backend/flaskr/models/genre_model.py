from flask import Blueprint, request, jsonify
import joblib
import numpy as np
import pandas as pd
from flaskr.services.data_preparation import prepare_data

genre_blueprint = Blueprint('genre', __name__)

# Load models and encoders
model = joblib.load('../machine_learning/genre_model_based_number_of_rating.pkl')
age_encoder = joblib.load('../machine_learning/age_ohe.pkl')
occupation_encoder = joblib.load('../machine_learning/occupation_ohe.pkl')
genre_columns = joblib.load('../machine_learning/genre_columns.pkl')
age_map = joblib.load('../machine_learning/age_map.pkl')


@genre_blueprint.route('/predict_genre', methods=['POST'])
def predict_genre():
    data = request.json
    gender = data.get('gender', 1)
    age = data.get('age', 28)
    occupation = data.get('occupation', "executive/managerial")

    input_features = prepare_data(age, occupation, gender, age_encoder, occupation_encoder, age_map)
    predictions = model.predict(input_features)
    predicted_genre_labels = [genre for genre, flag in zip(genre_columns, predictions[0]) if flag == 1]

    return jsonify({'predicted_genres': predicted_genre_labels})
