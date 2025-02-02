from fastapi import APIRouter

router = APIRouter(prefix="/statistics", tags=["crud"])

@router.get("/status-by-day/")
def get_row():
    return {"message": "retrieve"}

