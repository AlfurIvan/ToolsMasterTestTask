from fastapi import APIRouter

router = APIRouter(prefix="/statistics", tags=["statistics"])

@router.get("/status-by-day/")
def get_row():
    return {"message": "retrieve"}

