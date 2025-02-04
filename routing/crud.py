import asyncio

import httpx
import requests
from fastapi import APIRouter
from utils.coda import (
    timetracker_table as timetracker,
    coda_doc as doc,
    auth_header,
    BASE_URL,
    TOOLS_MASTER_DOC_ID,
    TIMETRACKER_TABLE_ID,
    timetracker_columns,

)

from schemas.base import TimetrackerRow

router = APIRouter(prefix="/table", tags=["crud"])


@router.get("/")
async def table():
    async with httpx.AsyncClient() as client:

        rows = await client.get(
            BASE_URL + f'/docs/{TOOLS_MASTER_DOC_ID}/tables/{TIMETRACKER_TABLE_ID}/rows?visibleOnly=false&useColumnNames=true',
            headers=auth_header
        )
    columns = timetracker_columns
    result = {
        "columns": columns['items'],
        "rows": rows.json()['items']
    }
    return result


@router.post("/new-row/")
async def new_row(data: list[TimetrackerRow]):
    restruct_data = {"rows": [_data.model_dump() for _data in data]}
    print(restruct_data)
    async with httpx.AsyncClient() as client:
        result = await client.post(
            BASE_URL + f'/docs/{TOOLS_MASTER_DOC_ID}/tables/{TIMETRACKER_TABLE_ID}/rows?disableParsing=false',
            data=restruct_data,
            headers=auth_header
        )
    if result.status_code != 200:
        print(result.status_code, result.json())
    return result.json()


@router.put("/update-row/")
async def update_row():
    return {"message": "update"}


@router.delete("/delete-row/")
async def delete_row():
    return {"message": "delete"}
