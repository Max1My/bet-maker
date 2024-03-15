from pydantic import BaseModel

from src.core.domain.events.enums import EventStatus


class UpdateStatusEventRequest(BaseModel):
    status: EventStatus
