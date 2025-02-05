import os

import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from routing.crud import router as crud_router
from routing.statistics_routes import router as statistics_router
app = FastAPI()


app.include_router(crud_router)
app.include_router(statistics_router)

@app.get("/")
async def root():
    return {'message': ''}
    # return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)