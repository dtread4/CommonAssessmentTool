from typing import Dict, List, Any

from fastapi import HTTPException

from app.clients.schema import PredictionInput
from app.clients.service.ml_model_manager import MLModelRepository, \
    MLModelManager
# from app.clients.service.ml_models_router import model_repository, model_manager
from app.clients.service.predicttion_service import \
    convert_prediction_input_to_client_base, predict_with_interventions

model_repository = MLModelRepository()
model_manager = MLModelManager(model_repository)
class PredictionController:
    @staticmethod
    def list_models() -> Dict[str, List[str]]:
        """List all available ML models"""
        return {
            "models": [str(model) for model in model_repository.list_models()]}

    @staticmethod
    def switch_model(model_name: str) -> Dict[str, str]:
        """Switch between ML models"""
        success = model_manager.switch_model(model_name)
        if not success:
            raise HTTPException(status_code=400, detail="Model switch failed")
        return {"message": f"Model switched to {model_name}"}

    @staticmethod
    def get_current_model() -> Dict[str, str]:
        """Get the current ML model"""
        return {"current_model": str(model_manager.get_current_model())}

    @staticmethod
    def predict_with_model(input_data: PredictionInput,
        model_name: str = None) -> Dict[str, Any]:
        """
        Generate prediction with intervention recommendations

        Args:
            input_data: Client data for prediction
            model_name: Optional name of model to use (uses current model if None)

        Returns:
            Dict with baseline prediction and intervention predictions
        """
        try:
            if model_name:
                model = model_repository.get_model_instance(model_name)
            else:
                model = model_manager.get_current_model()

            client = convert_prediction_input_to_client_base(input_data)
            return predict_with_interventions(model, client)
        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Prediction failed: {str(e)}") from e
