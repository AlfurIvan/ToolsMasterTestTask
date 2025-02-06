"""basic CRUD endpoints"""

import asyncio

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from schemas.docs import (
    CodaResponses,
)

from schemas.base import TimetrackerRow
from utils.utils import get_columns
from utils.coda_requests import (
    get_raw_columns,
    get_raw_rows,
    create_new_row,
    delete_row_by_id,
    update_row_by_id
)

router = APIRouter(prefix="/table", tags=["crud"])


@router.get("/")
async def table() -> CodaResponses:
    rows = await get_raw_rows(False)
    columns = await get_raw_columns()
    return CodaResponses(
        columns=columns.json()['items'],
        rows=rows.json()['items'],
        statuses=[columns.status_code, rows.status_code]
    )


@router.post("/new-row/")
async def new_row(data: list[TimetrackerRow]):
    restruct_data = await asyncio.gather(*[obj.render_to_cells() for obj in data])
    columns = await get_columns()
    prep_data = {"rows": restruct_data, "keyColumns": [columns["name"]["id"]]}
    response = await create_new_row(prep_data)
    return JSONResponse(content=response.json, status_code=response.status_code)


@router.put("/update-row/{row_id}")
async def update_row(row_id: str, data: TimetrackerRow):
    restruct_data = await data.render_to_cells()
    prep_data = {"row": restruct_data}
    response = await update_row_by_id(row_id, prep_data)
    return JSONResponse(content=response.json, status_code=response.status_code)


@router.delete("/delete-row/{row_id}")
async def delete_row(row_id: str):
    response = await delete_row_by_id(row_id)
    return JSONResponse(content=response.json, status_code=response.status_code)
