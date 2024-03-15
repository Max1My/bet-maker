from starlette import status

from src.core.domain.events import dto, errors
from src.core.domain.events.repository import EventRepository
from src.core.domain.events.requests import UpdateStatusEventRequest


class EventService:
    def __init__(
            self
    ) -> None:
        self.repository = EventRepository()

    async def create(self) -> dto.EventView:
        event_data = dto.EventCreate(
            status=None
        )
        return await self.repository.create(event_data)

    async def read(self, event_id) -> dto.EventView:
        return await self.repository.get(event_id)

    async def get_or_create(self, event_id: int) -> dto.EventView:
        event_model = await self.read(event_id=event_id)
        if not event_model:
            event_model = await self.create()
        return event_model

    async def update_status(self, event_id: int, request: UpdateStatusEventRequest):
        event = await self.read(event_id=event_id)
        if not event:
            raise errors.EventHTTPError(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Event with id {event_id} not found'
            )
        update_data = dto.EventUpdate(
            status=request.status.value
        )
        return await self.repository.update(update_data, event)
