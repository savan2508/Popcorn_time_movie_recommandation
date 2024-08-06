import numpy as np
import pandas as pd


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
