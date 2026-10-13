from fastapi import APIRouter

router = APIRouter(tags=["exams"])


@router.get("/exams")
def list_exams() -> list[dict[str, str]]:
    """STUB: replace with the bundled demo exams."""
    return [{"id": "demo-001"}, {"id": "demo-002"}]
