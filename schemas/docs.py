"""These schemas only for OpenAPI documentation"""
from pydantic import BaseModel, HttpUrl
from typing import Any


class Format(BaseModel):
    type: str
    isArray: bool
    format: str | None = None
    table: dict[str, Any] | None = None


class Column(BaseModel):
    id: str
    type: str
    name: str
    href: HttpUrl
    display: bool | None = None
    format: Format
    calculated: bool | None = None
    formula: str | None = None


class Row(BaseModel):
    id: str
    type: str
    href: HttpUrl
    name: str
    index: int
    createdAt: str
    updatedAt: str
    browserLink: HttpUrl
    values: dict[str, Any]


class CodaResponses(BaseModel):
    columns: list[Column]
    rows: list[Row]
    statuses: list[int]
