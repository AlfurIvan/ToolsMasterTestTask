import httpx

from config import CODA_API_KEY, TOOLS_MASTER_DOC_ID, BASE_URL, TIMETRACKER_TABLE_ID

auth_header = {'Authorization': 'Bearer ' + CODA_API_KEY}

async def get_raw_rows(use_column_names):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f'{BASE_URL}/docs/{TOOLS_MASTER_DOC_ID}/tables/{TIMETRACKER_TABLE_ID}/rows'
            f'?useColumnNames={"true" if use_column_names else "false"}',
            headers=auth_header
        )
        return resp.json()

async def get_raw_columns():
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f'{BASE_URL}/docs/{TOOLS_MASTER_DOC_ID}/tables/{TIMETRACKER_TABLE_ID}/columns',
            headers=auth_header
        )
        return resp.json()

async def create_new_row(row_data):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f'{BASE_URL}/docs/{TOOLS_MASTER_DOC_ID}/tables/{TIMETRACKER_TABLE_ID}/rows',
            json=row_data,
            headers={**auth_header, "Content-Type": "application/json"}
        )
        return resp.json()

async def update_row_by_id(row_id, row_data):
    async with httpx.AsyncClient() as client:
        resp = await client.put(
            f'{BASE_URL}/docs/{TOOLS_MASTER_DOC_ID}/tables/{TIMETRACKER_TABLE_ID}/rows/{row_id}',
            json=row_data,
            headers={**auth_header, "Content-Type": "application/json"}
        )
        return resp

async def delete_row_by_id(row_id):
    async with httpx.AsyncClient() as client:
        resp = await client.delete(
            f'{BASE_URL}/docs/{TOOLS_MASTER_DOC_ID}/tables/{TIMETRACKER_TABLE_ID}/rows/{row_id}',
            headers={**auth_header, "Content-Type": "application/json"}
        )
        return resp.json()