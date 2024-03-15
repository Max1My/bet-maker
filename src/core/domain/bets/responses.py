from decimal import Decimal

from pydantic import BaseModel, field_serializer

from src.core.domain.bets.enums import StatusBet


class BetCreatedResponse(BaseModel):
    bet_id: int


class Bet(BaseModel):
    event_id: int
    bet_id: int
    status: str
    amount: Decimal

    @field_serializer("status")
    def serialize_status(self, status: str, _info):
        return StatusBet[status].value[1]


class BetsResponse(BaseModel):
    bets: list[Bet]
