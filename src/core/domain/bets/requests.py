from decimal import Decimal
from pydantic import BaseModel, Field


class CreateBetRequest(BaseModel):
    event_id: int
    bet_amount: Decimal = Field(ge=0.1, max_digits=12, decimal_places=2)
