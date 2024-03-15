from sqlalchemy import select

from src.common.base_repository import BaseRepository
from src.core.domain.events import dto, models


class EventRepository(BaseRepository):
    database_model = models.Event
    view_model = dto.EventView

    def __init__(self):
        super().__init__()
        self.base_stmt = self.__base_stmt()

    def __base_stmt(self):
        stmt = (
            select(self.database_model)
        )
        return stmt

    async def create(self, data: dto.EventCreate):
        async with self.session() as session:
            async with session.begin():
                model = self._pydantic_to_model(data, self.database_model())
                session.add(model)
                await session.commit()
            await session.refresh(model)
            return model

    async def get(self, event_id: int):
        async with self.session() as session:
            async with session.begin():
                stmt = (
                    self.base_stmt
                    .where(self.database_model.id == event_id)
                )
                item = (await session.scalars(stmt)).unique().first()
                if item:
                    return self._model_to_pydantic(item, self.view_model)
                else:
                    await session.close()

    async def update(self, update_data: dto.EventUpdate, event: dto.EventView):
        async with self.session() as session:
            async with session.begin():
                model = self._pydantic_to_model(event, self.database_model())
                update_model = self._pydantic_to_model(update_data, model)
                updated_item = await session.merge(update_model)
            await session.commit()
            return updated_item
