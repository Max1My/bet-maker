from fastapi import APIRouter
from starlette import status

from src.core.domain.bets import requests, responses, errors
from src.core.domain.bets.service import BetService

bets_router = APIRouter()
service = BetService()


@bets_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    tags=['BETS'],
    name='Create bet'
)
async def create_bet(
        request: requests.CreateBetRequest
) -> responses.BetCreatedResponse:
    bet_model = await service.create(request)
    if not bet_model:
        raise errors.BetHTTPError(
            status_code=status.HTTP_409_CONFLICT,
            detail='Bet Create failed'
        )
    return responses.BetCreatedResponse(
        bet_id=bet_model.id
    )


@bets_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    tags=['BETS'],
    name='Get bets',
)
async def get_bets() -> responses.BetsResponse:
    bets_models = await service.get_all_bets()
    if bets_models is None:
        raise errors.BetHTTPError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Bets not found'
        )
    return responses.BetsResponse(
        bets=[
            responses.Bet(
                event_id=bet.event_id,
                bet_id=bet.id,
                status=bet.status,
                amount=bet.amount
            ) for bet in bets_models
        ]
    )
