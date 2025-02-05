import asyncio
import re

import httpx
from envparse import env

env.read_envfile('.env')

CODA_API_KEY = env('CODA_API_KEY')
TOOLS_MASTER_DOC_ID = env('TOOLS_MASTER_DOC_ID')
TIMETRACKER_TABLE_ID = env('TIMETRACKER_TABLE_ID')
BASE_URL = "https://coda.io/apis/v1"
auth_header = {'Authorization': 'Bearer ' + CODA_API_KEY}


def to_snake_case(name: str) -> str:
    return re.sub(r'[\s\-]+', '_', name.strip()).lower()


async def get_raw_columns():
    async with httpx.AsyncClient() as client:
        raw_columns = await client.get(
            f'{BASE_URL}/docs/{TOOLS_MASTER_DOC_ID}/tables/{TIMETRACKER_TABLE_ID}/columns',
            headers=auth_header
        )
        return raw_columns.json()


async def get_columns():
    columns = {
        "name": None,
        "actual_completion_date": None,
        "planned_completion_date": None,
        "status": None,
        "category": None,
    }

    raw_columns = await get_raw_columns()
    for item in raw_columns['items']:
        columns[to_snake_case(item['name'])] = {"id": item['id'], "name": item['name']}
    return columns
