from typing import List, Dict, Any

import numpy as np

from app.clients.schema import PredictionInput, ClientBase, Gender
from app.clients.service.constants import INTERVENTION_NAMES, \
    DEFAULT_INTERVENTION_COMBINATIONS, INTERVENTION_FIELDS, \
    FIELDS_WITH_LOW_AT_ONE
from app.clients.service.constants import BOOL_FIELDS


def convert_prediction_input_to_client_base(
    input_data: PredictionInput) -> ClientBase:
    """Convert PredictionInput to ClientBase"""
    # Create a dictionary for ClientBase
    client_dict = {}

    for field, value in input_data.dict().items():
        if field == "gender":
            # Convert gender string to Gender enum
            client_dict[field] = Gender.MALE if value.lower() in ["male", "m",
                                                                  "1"] else Gender.FEMALE

        elif field in BOOL_FIELDS:
            # Convert string booleans to actual booleans
            if isinstance(value, str):
                client_dict[field] = value.lower() in ["true", "yes", "1", "t",
                                                       "y"]
            else:
                client_dict[field] = bool(value)
        else:
            # Convert to integer
            try:
                client_dict[field] = int(value)
            except (ValueError, TypeError):
                # Set defaults if conversion fails
                if field in FIELDS_WITH_LOW_AT_ONE:
                    client_dict[field] = 1  # Default to lowest level
                else:
                    client_dict[field] = 0  # Default for other fields

    return ClientBase(**client_dict)


def client_base_to_feature_list(client: ClientBase,
    interventions: Dict[str, bool] = None) -> List[float]:
    """Convert ClientBase object to feature list for model prediction"""
    # Default interventions to empty dict if None
    if interventions is None:
        interventions = {}

    # Convert boolean values to 0/1 floats
    features = [
        float(client.age),
        # Convert Gender enum to 0/1
        float(1 if client.gender == Gender.MALE else 0),
        float(client.work_experience),
        float(client.canada_workex),
        float(client.dep_num),
        float(1 if client.canada_born else 0),
        float(1 if client.citizen_status else 0),
        float(client.level_of_schooling),
        float(1 if client.fluent_english else 0),
        float(client.reading_english_scale),
        float(client.speaking_english_scale),
        float(client.writing_english_scale),
        float(client.numeracy_scale),
        float(client.computer_scale),
        float(1 if client.transportation_bool else 0),
        float(1 if client.caregiver_bool else 0),
        float(client.housing),
        float(client.income_source),
        float(1 if client.felony_bool else 0),
        float(1 if client.attending_school else 0),
        float(1 if client.currently_employed else 0),
        float(1 if client.substance_use else 0),
        float(client.time_unemployed),
        float(1 if client.need_mental_health_support_bool else 0),
    ]

    for field in INTERVENTION_FIELDS:
        features.append(float(1 if interventions.get(field, False) else 0))

    return features


def predict_with_interventions(
    model,
    client: ClientBase,
    intervention_combinations: List[Dict[str, bool]] = None
) -> Dict[str, Any]:
    """
    Generate predictions with different intervention combinations.
    """
    if intervention_combinations is None:
        intervention_combinations = DEFAULT_INTERVENTION_COMBINATIONS

    model.load_if_trained()

    # Prediction with no intervention
    baseline_features = client_base_to_feature_list(client)
    baseline_prediction = model.predict(np.array([baseline_features]))
    baseline_score = float(baseline_prediction[0])

    # Test each intervention combination
    interventions_results = []
    for combo in intervention_combinations:
        # Predict with interventions
        combo_features = client_base_to_feature_list(client, combo)
        combo_prediction = model.predict(np.array([combo_features]))
        combo_score = float(combo_prediction[0])

        # Create list of intervention names for this combination
        intervention_names_list = [INTERVENTION_NAMES[intervention] for
                                   intervention in combo.keys()]

        # Add to results
        interventions_results.append([
            round(combo_score, 2),  # 2 decimal place
            intervention_names_list
        ])

    # Construct the response
    response = {
        "baseline": baseline_score,
        "interventions": interventions_results
    }

    return response
