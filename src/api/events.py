from fastapi import APIRouter
from starlette import status

from src.core.domain.events import requests, errors
from src.core.domain.bets.service import BetService
from src.core.domain.events.service import EventService

events_router = APIRouter()
service = EventService()
bet_service = BetService()


@events_router.post(
    path="/{event_id}",
    status_code=status.HTTP_200_OK,
    tags=['EVENTS'],
    name='Update event'
)
async def update_event(
        event_id: int,
        request: requests.UpdateStatusEventRequest
):
    await service.update_status(event_id=event_id, request=request)
    bet_model = await bet_service.update_status(request=request, event_id=event_id)
    if not bet_model:
        raise errors.EventHTTPError(
            status_code=status.HTTP_409_CONFLICT,
            detail='Update event failed'
        )
