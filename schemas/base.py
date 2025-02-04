from enum import Enum

from pydantic import BaseModel, Field, BeforeValidator, ValidationError
from typing import Annotated, Any
import re

date_pattern = re.compile(r"^(0?[1-9]|1[0-2])/(0?[1-9]|[12][0-9]|3[01])/\d{4}$")


def validate_date(value):
    if value is not None:
        try:
            date_pattern.match(value)
        except ValueError:
            raise ValidationError("Date must be in the format MM/DD/YYYY")
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
    parent: list[str] | None
    subitems: list[str] | None

    def model_dump(self, *args, **kwargs) -> dict[str, Any]:
        """Add merging into this form of json:
            {
              "rows": [
                {
                  "cells": [
                    {
                      "column": "c-tuVwxYz",
                      "value": "string"
                    }
                  ]
                }
              ],
              "keyColumns": [
                "c-bCdeFgh"
              ]
            }
            """
        return super().model_dump(*args, **kwargs)
