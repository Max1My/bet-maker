from fastapi import APIRouter

from .bets import bets_router
from .events import events_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(router=bets_router, prefix="/bets")
api_router.include_router(router=events_router, prefix="/events")
