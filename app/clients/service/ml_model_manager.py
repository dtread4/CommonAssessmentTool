from typing import List

from app.clients.service.ml_models import InterfaceMLModelRepository, \
    LinearRegressionModel, RandomForestModel, SVMModel, InterfaceBaseMLModel, \
    InterfaceMLModelManager


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

