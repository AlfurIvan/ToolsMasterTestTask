"""Statistic endpoints"""

from collections import defaultdict
from datetime import datetime
from typing import Any

from fastapi import APIRouter

from schemas.base import StatusChoices, CategoryChoices
from utils.coda_requests import get_raw_rows

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("/status-by-day/")
async def status_by_day() -> dict[str, dict[str, int | Any]]:
    resp = await get_raw_rows(True)

    if resp.status_code != 200:
        return resp.json()

    rows = resp.json()
    status_by_day_count: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for item in rows.get("items", []):
        values = item.get("values", {})

        actual_completion = values.get("Actual Completion Date")
        status = values.get("Status")
        date = actual_completion.split("T")[0]

        try:
            status_enum = StatusChoices(status)
            status_by_day_count[date][status_enum.value] += 1
        except ValueError:
            pass

    return {"status_by_day": {date: dict(counts) for date, counts in status_by_day_count.items()}}


@router.get("/type-distribution/")
async def type_distribution_percentage() -> dict[str, dict[str, float | int]]:
    resp = await get_raw_rows(True)

    if resp.status_code != 200:
        return resp.json()

    rows = resp.json()
    category_count: dict[str, int] = defaultdict(int)
    total_items = len(rows.get("items", []))

    for item in rows.get("items", []):
        category = item.get("values", {}).get("Category")

        if category:
            try:
                category_enum = CategoryChoices(category)
                category_count[category_enum.value] += 1
            except ValueError:
                pass

    type_distribution = {}
    for category, count in category_count.items():
        percentage = (count / total_items) * 100 if total_items > 0 else 0
        type_distribution[category] = round(percentage, 2)

    return {"type_distribution": type_distribution}


@router.get("/deadline-exceeding-by-day/")
async def deadline_exceeding_by_day():
    resp = await get_raw_rows(True)

    if resp.status_code != 200:
        return resp.json()

    rows = resp.json()
    deadline_exceeded = defaultdict(int)

    for item in rows.get("items", []):
        values = item.get("values", {})
        planned_completion = values.get("Planned Completion Date", "")
        actual_completion = values.get("Actual Completion Date", "")
        status = values.get("Status")


        planned_date = datetime.fromisoformat(planned_completion[:19]) if planned_completion else None
        actual_date = datetime.fromisoformat(actual_completion[:19]) if actual_completion else None

        if planned_date and status not in ["TODO", "Not Started"]:
            if datetime.today() > planned_date and (actual_date is None or actual_date > planned_date):
                date = planned_date.date().isoformat()
                deadline_exceeded[date] += 1
    unsorted_result = dict(deadline_exceeded)
    return {"deadline_exceeding_by_day": dict(sorted(unsorted_result.items()))}
