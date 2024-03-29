# generated by fastapi-codegen:
#   filename:  .\openapi_v1.0.1.yaml
#   timestamp: 2024-01-26T14:05:16+00:00

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict
import typing
import re
from pydantic import BaseModel, Field, TypeAdapter

class Event(BaseModel):
    id: int = Field(..., example=10)
    event_date: datetime
    attribute1: Optional[int] = Field(None, example=198772)
    attribute2: Optional[int] = Field(None, example=198772)
    attribute3: Optional[int] = Field(None, example=198772)
    attribute4: Optional[str] = Field(None, example='some string')
    attribute5: Optional[str] = Field(None, example='12345')
    attribute6: Optional[bool] = None
    metric1: int = Field(..., example=198772)
    metric2: float = Field(..., example=1.2)


class Filter:
    attribute: str
    value: str
    @classmethod
    def parser(cls,
               string):
        _pattern = "^attribute:(.*),value:(.*)$"
        _match = re.match(_pattern, string)
        _attribute = _match.groups()[0]
        _type=str
        if (_attribute in Event.model_fields):
            if (type(Event.model_fields[_attribute].annotation) is typing._UnionGenericAlias):
                _type = Event.model_fields[_attribute].annotation.__args__[0]
            else:
                _type = Event.model_fields[_attribute].annotation
            if (_type is bool):
                print(f"found bool and {TypeAdapter(bool).validate_python(_match.groups()[1])}")
                _type = TypeAdapter(bool).validate_python
        else:
            raise ValueError(f"Filter {_attribute} is not allowed")
        return {"attribute":_attribute, "value":_type(_match.groups()[1])}

class Granularity(Enum):
    hourly = 'hourly'
    daily = 'daily'


class Filters:
    filters: Optional[List[Filter]] = None
    @classmethod
    def parser(
        cls, 
         filters: Optional[List[Filter]] = None
    ) -> Dict:
        return {"filters": filters}


class Granularity1(Enum):
    hourly = 'hourly'
    daily = 'daily'
