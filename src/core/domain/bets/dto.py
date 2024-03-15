from decimal import Decimal

from pydantic import Field, BaseModel

from src.common.base_model import PydanticBaseModel
from src.core.domain.events.dto import EventView


class Bet(PydanticBaseModel):
    event_id: int
    amount: Decimal
    status: str


class BetView(Bet):
    event: EventView | None = Field(exclude=True, example="")


class BetCreate(BaseModel):
    event_id: int
    amount: Decimal
    status: str


class BetUpdate(BaseModel):
    status: str
