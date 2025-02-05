import asyncio

import httpx
from fastapi import APIRouter

from schemas.docs import (
    CodaResponses,
    CodaCreateResponse,
    CodaUpdateDeleteResponse
)
from utils.coda import (
    auth_header,
    BASE_URL,
    TOOLS_MASTER_DOC_ID,
    TIMETRACKER_TABLE_ID,
    get_columns,
    get_raw_columns,

)

from schemas.base import TimetrackerRow

router = APIRouter(prefix="/table", tags=["crud"])


@router.get("/")
async def table() -> CodaResponses:
    async with httpx.AsyncClient() as client:
        rows = await client.get(
            f'{BASE_URL}/docs/{TOOLS_MASTER_DOC_ID}/tables/{TIMETRACKER_TABLE_ID}/rows?visibleOnly=false&useColumnNames=true',
            headers=auth_header
        )
        columns = await get_raw_columns()
        result = CodaResponses(
            columns=columns['items'],
            rows=rows.json()['items']
        )
        return result


@router.post("/new-row/")
async def new_row(data: list[TimetrackerRow]) -> CodaCreateResponse:
    restruct_data = await asyncio.gather(*[obj.render_to_cells() for obj in data])
    columns = await get_columns()
    prep_data = {"rows": restruct_data, "keyColumns": [columns["name"]["id"]]}
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f'{BASE_URL}/docs/{TOOLS_MASTER_DOC_ID}/tables/{TIMETRACKER_TABLE_ID}/rows',
            json=prep_data,
            headers={**auth_header, "Content-Type": "application/json"}
        )
        return resp.json()


@router.put("/update-row/{row_id}")
async def update_row(row_id: str, data: TimetrackerRow)-> CodaUpdateDeleteResponse:
    restruct_data = await data.render_to_cells()
    prep_data = {"row": restruct_data}
    async with httpx.AsyncClient() as client:
        resp = await client.put(
            f'{BASE_URL}/docs/{TOOLS_MASTER_DOC_ID}/tables/{TIMETRACKER_TABLE_ID}/rows/{row_id}',
            json=prep_data,
            headers={**auth_header, "Content-Type": "application/json"}
        )
    return resp.json()


@router.delete("/delete-row/{row_id}")
async def delete_row(row_id: str) -> CodaUpdateDeleteResponse:
    async with httpx.AsyncClient() as client:
        resp = await client.delete(
            f'{BASE_URL}/docs/{TOOLS_MASTER_DOC_ID}/tables/{TIMETRACKER_TABLE_ID}/rows/{row_id}',
            headers={**auth_header, "Content-Type": "application/json"}
        )
    return resp.json()
