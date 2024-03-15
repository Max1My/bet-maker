from src.core.domain.bets import requests, dto
from src.core.domain.bets.enums import StatusBet
from src.core.domain.bets.repository import BetRepository
from src.core.domain.events.requests import UpdateStatusEventRequest
from src.core.domain.events.service import EventService


class BetService:
    def __init__(
            self
    ) -> None:
        self.repository = BetRepository()
        self.event_service = EventService()

    async def create(self, request: requests.CreateBetRequest) -> dto.BetView:
        event = await self.event_service.get_or_create(event_id=request.event_id)
        bet_data = dto.BetCreate(
            event_id=event.id,
            amount=request.bet_amount,
            status=StatusBet.NOT_PLAYED_YET.value[0]
        )
        return await self.repository.create(bet_data)

    async def get_all_bets(self) -> list[dto.BetView]:
        return await self.repository.get_all()

    async def get_bets_by_event_id(self, event_id: int) -> list[dto.BetView]:
        return await self.repository.get_by_event_id(event_id=event_id)

    async def update_status(self, event_id: int, request: UpdateStatusEventRequest):
        bet_ids = [bet_model.id for bet_model in await self.get_bets_by_event_id(event_id)]
        bet_data = dto.BetUpdate(
            status=request.status
        )
        return await self.repository.update_status(bet_data, bet_ids)

    async def set_winner(self, event_id: int):
        bet_data = dto.BetUpdate(
            status=StatusBet.WIN.value[0]
        )
        bet_ids = [bet_model.id for bet_model in await self.get_bets_by_event_id(event_id)]
        return await self.repository.update_status(bet_data, bet_ids)

    async def set_loss(self, event_id: int):
        bet_data = dto.BetUpdate(
            status=StatusBet.LOSE.value[0]
        )
        bet_ids = [bet_model.id for bet_model in await self.get_bets_by_event_id(event_id)]
        return await self.repository.update_status(bet_data, bet_ids)
