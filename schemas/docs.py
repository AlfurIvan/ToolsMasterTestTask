"""These schemas only for OpenAPI documentation"""
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Any


class Format(BaseModel):
    type: str
    isArray: bool
    format: Optional[str] = None
    table: Optional[Dict[str, Any]] = None


class Column(BaseModel):
    id: str
    type: str
    name: str
    href: HttpUrl
    display: Optional[bool] = None
    format: Format
    calculated: Optional[bool] = None
    formula: Optional[str] = None


class Row(BaseModel):
    id: str
    type: str
    href: HttpUrl
    name: str
    index: int
    createdAt: str
    updatedAt: str
    browserLink: HttpUrl
    values: Dict[str, Any]


class CodaResponses(BaseModel):
    columns: List[Column]
    rows: List[Row]


class CodaCreateResponse(BaseModel):
    requestId: str


class CodaUpdateDeleteResponse(BaseModel):
    id: str
    requestId: str
