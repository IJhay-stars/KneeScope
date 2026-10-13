from knee_api.schemas.predict import FindingScore, PredictionResponse
from kneeml.constants import MODEL_VERSION
from kneeml.inference.predict import predict_exam


def run_prediction(exam_id: str) -> PredictionResponse:
    scores = predict_exam(exam_id)
    return PredictionResponse(
        exam_id=exam_id,
        model_version=MODEL_VERSION,
        findings=[FindingScore(name=n, probability=p) for n, p in scores.items()],
    )
