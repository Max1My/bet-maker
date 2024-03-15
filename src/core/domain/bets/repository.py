from sqlalchemy.orm import joinedload

from src.common.base_repository import BaseRepository
from src.core.domain.bets import dto, models
from sqlalchemy import select, update


class BetRepository(BaseRepository):
    database_model = models.Bet
    view_model = dto.BetView

    def __init__(self):
        super().__init__()
        self.base_stmt = self.__base_stmt()

    def __base_stmt(self):
        stmt = (
            select(self.database_model)
            .options(
                joinedload(self.database_model.event)
            )
        )
        return stmt

    async def create(self, data: dto.BetCreate):
        async with self.session() as session:
            async with session.begin():
                model = self._pydantic_to_model(data, self.database_model())
                session.add(model)
                await session.commit()
            await session.refresh(model)
            return model

    async def get_all(self):
        async with self.session() as session:
            async with session.begin():
                items = (await session.scalars(self.base_stmt)).unique().all()
                if items:
                    return [self._model_to_pydantic(item, self.view_model) for item in items]
                else:
                    await session.close()

    async def get_by_event_id(self, event_id: int):
        async with self.session() as session:
            async with session.begin():
                stmt = (
                    self.base_stmt
                    .where(self.database_model.event_id == event_id)
                )
                items = (await session.scalars(stmt)).unique().all()
                if items:
                    return [self._model_to_pydantic(item, self.view_model) for item in items]
                else:
                    await session.close()

    async def update_status(self, update_data: dto.BetUpdate, bet_ids: list):
        async with self.session() as session:
            async with session.begin():
                stmt = (
                    update(self.database_model)
                    .where(self.database_model.id.in_(bet_ids))
                    .values(status=update_data.status)
                )
                await session.execute(stmt)
                await session.commit()
                return True
