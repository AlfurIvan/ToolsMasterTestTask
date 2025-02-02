from fastapi import APIRouter

router = APIRouter(prefix="/table", tags=["crud"])




@router.get("/")
def table():
    return {"message": "retrieve"}

@router.post("/new-row/")
def new_row():
    return {"message": "create"}

@router.put("/update-row/")
async def update_row():
    return {"message": "update"}

@router.delete("/delete-row/")
async def delete_row():
    return {"message": "delete"}
