from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    exam_id: str


class FindingScore(BaseModel):
    name: str
    probability: float = Field(ge=0, le=1)
    key_slices: list[int] = []


class PredictionResponse(BaseModel):
    exam_id: str
    model_version: str
    findings: list[FindingScore]
    disclaimer: str = "Research prototype. Not for clinical use."
