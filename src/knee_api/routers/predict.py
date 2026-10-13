from fastapi import APIRouter

from knee_api.schemas.predict import PredictionResponse, PredictRequest
from knee_api.services.prediction import run_prediction

router = APIRouter(tags=["predict"])


@router.post("/predict", response_model=PredictionResponse)
def predict(body: PredictRequest) -> PredictionResponse:
    return run_prediction(body.exam_id)
