import os
from abc import ABC, abstractmethod
from typing import List

import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR

from app.clients.service.model_helper import get_all_feature_columns, get_true_file_name

default_unformatted_model_path = os.path.join(
    os.path.dirname(__file__), "pretrained_models", "model_{}.pkl"
)


class InterfaceBaseMLModel(ABC):
    """Interface of a base ML Model"""

    def __init__(self):
        self.feature_columns = get_all_feature_columns()

    @abstractmethod
    def fit(self, features: np.ndarray, targets: np.ndarray):
        """Fit the model to provided data"""

    @abstractmethod
    def predict(self, features: np.ndarray) -> np.ndarray:
        """Predict using the fitted model"""

    def save(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path: str):
        with open(path, "rb") as f:
            return pickle.load(f)

    @abstractmethod
    def __str__(self) -> str:
        """Return the name of the model"""

    def load_if_trained(self):
        pass


class LinearRegressionModel(InterfaceBaseMLModel):
    def __init__(self):
        super().__init__()
        self.model = LinearRegression()

    def fit(self, features, targets):
        self.model.fit(features, targets)

    def predict(self, features):
        return self.model.predict(features)

    def __str__(self):
        return "Linear Regression"

    def load_if_trained(self):
        path = get_true_file_name(str(self), default_unformatted_model_path)
        print(f"Attempting to load model from: {path}")
        if os.path.exists(path):
            print("Model file exists, loading...")
            self.model = InterfaceBaseMLModel.load(path)
        else:
            print(f"Model file not found at {path}")


class RandomForestModel(InterfaceBaseMLModel):
    def __init__(self, n_estimators=100, random_state=42):
        super().__init__()
        self.model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)

    def fit(self, features, targets):
        self.model.fit(features, targets)

    def predict(self, features):
        return self.model.predict(features)

    def __str__(self):
        return "Random Forest Regressor"

    def load_if_trained(self):
        path = get_true_file_name(str(self), default_unformatted_model_path)
        print(f"Attempting to load model from: {path}")
        if os.path.exists(path):
            print("Model file exists, loading...")
            self.model = InterfaceBaseMLModel.load(path)
        else:
            print(f"Model file not found at {path}")


class SVMModel(InterfaceBaseMLModel):
    def __init__(self):
        super().__init__()
        self.model = SVR()

    def fit(self, features, targets):
        self.model.fit(features, targets)

    def predict(self, features):
        return self.model.predict(features)

    def __str__(self):
        return "SVM"

    def load_if_trained(self):
        path = get_true_file_name(str(self), default_unformatted_model_path)
        print(f"Attempting to load model from: {path}")
        if os.path.exists(path):
            print("Model file exists, loading...")
            self.model = InterfaceBaseMLModel.load(path)
        else:
            print(f"Model file not found at {path}")


class InterfaceMLModelRepository(ABC):
    """Interface for ML Models storage"""
    @abstractmethod
    def list_models(self) -> List[InterfaceBaseMLModel]:
        """Get list of all available models instances"""

    @abstractmethod
    def is_model_available(self, model_name: str) -> bool:
        """Check if a model is valid"""

    @abstractmethod
    def get_model_instance(self, model_name: str) -> InterfaceBaseMLModel:
        """Return an instance of the requested model"""


class InterfaceMLModelManager(ABC):
    """Interface for ML model management"""

    @abstractmethod
    def get_current_model(self) -> InterfaceBaseMLModel:
        """Get the current active ml model"""

    @abstractmethod
    def switch_model(self, model_name: str) -> bool:
        """Switch between models"""


class MLModelRepository(InterfaceMLModelRepository):
    def __init__(self):
        self._model_map = {
            "Linear Regression": LinearRegressionModel,
            "Random Forest Regressor": RandomForestModel,
            "Support Vector Machine": SVMModel,
        }

    def list_models(self) -> List[InterfaceBaseMLModel]:
        return [model_class() for model_class in self._model_map.values()]

    def is_model_available(self, model_name: str) -> bool:
        return model_name in self._model_map

    def get_model_instance(self, model_name: str) -> InterfaceBaseMLModel:
        if not self.is_model_available(model_name):
            raise ValueError(f"Model '{model_name}' is not available.")
        return self._model_map[model_name]()


class MLModelManager(InterfaceMLModelManager):
    def __init__(self, repository: InterfaceMLModelRepository):
        self._repository = repository
        self._current_model = repository.get_model_instance("Random Forest Regressor")

    def get_current_model(self) -> InterfaceBaseMLModel:
        return self._current_model

    def switch_model(self, model_name: str) -> bool:
        if self._repository.is_model_available(model_name):
            self._current_model = self._repository.get_model_instance(model_name)
            return True
        return False
