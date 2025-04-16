from typing import Dict, Any

from fastapi import APIRouter

from app.clients.schema import PredictionInput
from app.clients.service.prediction_controller import PredictionController

router = APIRouter(prefix="/ml_models", tags=["model"])

controller = PredictionController()


@router.get("/list", response_model=Dict[str, Any])
def list_models():
    """List all available ML models"""
    return controller.list_models()


@router.post("/switch/{model_name}", response_model=Dict[str, str])
def switch_models(model_name: str):
    """Switch between ML models"""
    return controller.switch_model(model_name)


@router.get("/current", response_model=Dict[str, str])
def current_model():
    """Get the current ML model"""
    return controller.get_current_model()


@router.post("/predict/{model_name}", response_model=Dict[str, Any])
def predict_with_model_name(input_data: PredictionInput, model_name: str):
    """
    Predict based on a given ML model name with intervention recommendations
    """
    return controller.predict_with_model(input_data, model_name)


@router.post("/predict", response_model=Dict[str, Any])
def predict_with_current_model(input_data: PredictionInput):
    """
    Predict based on current ML model with intervention recommendations

    Returns a dict with:
    - baseline: The baseline success rate without interventions
    - interventions: A list of [success_rate, intervention_names] pairs
    """
    return controller.predict_with_model(input_data)
