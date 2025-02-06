"""Other utils"""
import re

from utils.coda_requests import get_raw_columns


def to_snake_case(name: str) -> str:
    return re.sub(r'[\s\-]+', '_', name.strip()).lower()


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
