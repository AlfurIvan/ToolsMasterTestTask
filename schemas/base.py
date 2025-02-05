import re
from pydantic import BaseModel, Field, ValidationError, BeforeValidator
from typing import Annotated, Any
from enum import Enum
from utils.coda import get_columns

date_pattern = re.compile(r"^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}$")


def validate_date(value: str | None) -> str | None:
    if value is not None:
        if not date_pattern.match(value):
            raise ValueError("Date must be in the format MM/DD/YYYY")
    return value


class StatusChoices(str, Enum):
    todo = 'TODO'
    in_progress = 'In Progress'
    testing = 'Testing'
    done = 'Done'
    obsolete_dropped = 'Obsolete/Dropped'
    on_hold = 'On Hold'
    not_started = 'Not Started'
    blocked = 'Blocked'


class CategoryChoices(str, Enum):
    task = 'Task'
    subtask = 'Subtask'
    bug = 'Bug'


class TimetrackerRow(BaseModel):
    name: str = Field(..., title="Name")
    actual_completion_date: Annotated[str | None, BeforeValidator(validate_date)]
    planned_completion_date: Annotated[str | None, BeforeValidator(validate_date)]
    status: StatusChoices
    category: CategoryChoices

    async def render_to_cells(self) -> dict[str, Any]:
        columns = await get_columns()
        cells = {"cells": []}

        for key, value in self.model_dump().items():
            if isinstance(value, Enum):
                value = value.value

            cells["cells"].append({"column": columns[key]["id"], "value": value})
        return cells


a = {"rows": [{"cells": [{"column": "c-9Bfo0aSGnz", "value": "Dummy Task"}, {"column": "c-r7bi0XF3pC", "value": "02/05/2025"}, {"column": "c-Tqvhip3mKt", "value": "02/05/2025"}, {"column": "c-Urlbh_l_8Y", "value": "TODO"}, {"column": "c-GbGIoLn4jN", "value": "Task"}, {"column": "c-xG14mYU11m", "value": []}, {"column": "c-DmPpZrMb1l", "value": []}]}], "keyColumns": "c-9Bfo0aSGnz"}
