from pydantic import BaseModel

from src.common.base_model import PydanticBaseModel


class Event(PydanticBaseModel):
    status: str | None = None


class EventView(Event):
    ...


class EventCreate(BaseModel):
    status: str | None = None


class EventUpdate(EventCreate):
    ...
