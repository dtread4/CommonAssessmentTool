"""
Model training module for the Common Assessment Tool.
Handles the preparation, training, and saving of the prediction model.
Pass in model name via command line
"""

import os

# Standard library imports
import pickle
import sys

# Third-party imports
import numpy as np
import pandas as pd

# Local imports
# from sklearn import svm
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from app.clients.service.constants import COLUMNS_FIELDS, INTERVENTION_FIELDS
from app.clients.service.ml_model_manager import MLModelRepository
from .ml_models import (
    InterfaceBaseMLModel,
    LinearRegressionModel,
    RandomForestModel,
    SVMModel,
)

repo = MLModelRepository()

DEFAULT_UNFORMATTED_MODEL_PATH = "pretrained_models" + os.sep + "model_{}.pkl"


def get_model_by_name(model_type: str, n_estimators=100, random_state=42) -> InterfaceBaseMLModel:
    model_map = {
        "Linear Regression": LinearRegressionModel,
        "Random Forest Regressor": lambda: RandomForestModel(n_estimators, random_state),
        "Support Vector Machine": SVMModel,
    }

    if model_type not in model_map:
        print(f"ERROR! Invalid model type '{model_type}' passed in.")
        print(f"Available models: {repo.list_models()}")
        sys.exit(-1)

    constructor = model_map[model_type]
    return constructor() if callable(constructor) else constructor()


def prepare_model_data(test_size=0.2, random_state=42):
    """
    Prepare and train the Random Forest model using the dataset.
    Args:
        test_size: The percent of the dataset to use as test data (rest will be used as train data)
        random_state: The random state to generate train/test split with

    Returns:
        RandomForestRegressor: Trained model for predicting success rates
    """
    # Load dataset
    data = pd.read_csv("data_commontool.csv")

    # Combine all feature columns
    all_features = COLUMNS_FIELDS + INTERVENTION_FIELDS
    # Prepare training data
    features = np.array(data[all_features])  # Input features for the model
    targets = np.array(data["success_rate"])  # Target variable
    # Split the dataset
    feature_train, feature_test, target_train, target_test = train_test_split(
        # Removed unused variables
        features,
        targets,
        test_size=test_size,
        random_state=random_state,
    )

    return feature_train, feature_test, target_train, target_test


def train_model(
    feature_train, target_train, model_type, n_estimators=100, random_state=42
) -> InterfaceBaseMLModel:
    """
    Trains the model
    Args:
        feature_train: Training features
        target_train:  Target features
        model_type:     Which model to create
        n_estimators:   Number estimators (for random forest)
        random_state:   Random state to train with (for random forest)

    Returns: A trained model of the type specified

    """
    model = get_model_by_name(model_type, n_estimators, random_state)
    model.fit(feature_train, target_train)
    return model


def get_true_file_name(model_type, filename):
    """
    Takes a model type and file name, formats model type, and replaces spaces with underscores
    Args:
        model_type: The model type as a String
        filename: The file name (should follow 'model_{}.pkl' format)

    Returns: The clean file name
    """
    return filename.format(model_type).replace(" ", "_")


def save_model(model, model_type, filename=DEFAULT_UNFORMATTED_MODEL_PATH):
    """
    Save the trained model to a file.

    Args:
        model: Trained model to save
        model_type: The type of model being saved
        filename (str): Name of the file to save the model to
    """
    true_file_name = get_true_file_name(model_type, filename)
    with open(true_file_name, "wb") as model_file:
        pickle.dump(model, model_file)


def load_model(model_type, filename=DEFAULT_UNFORMATTED_MODEL_PATH):
    """
    Load a trained model from a file.

    Args:
        model_type: The type of model being loaded
        filename (str): Name of the file to load the model from

    Returns:
        The loaded model
    """
    true_file_name = get_true_file_name(model_type, filename)
    with open(true_file_name, "rb") as model_file:
        return pickle.load(model_file)


def main(argv):
    """Main function to train and save the model."""
    # Get the model type from the command line arguments
    model_type = argv[1]

    # Train and save the model
    print(f"Starting model training for {model_type} model...")
    # feature_train, feature_test, target_train, target_test = prepare_model_data()
    feature_train, _, target_train, _ = prepare_model_data()
    model = train_model(feature_train, target_train, model_type)
    save_model(model, model_type)
    print("Model training completed and saved successfully.")


if __name__ == "__main__":
    main(sys.argv)
