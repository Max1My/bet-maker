from sqlalchemy import Column, Numeric, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.mixins.models import PrimaryKeyMixin
from src.core.domain.events.models import Event
from src.db.engine import Base


class Bet(Base, PrimaryKeyMixin):
    __tablename__ = "bet"
    amount = Column(Numeric(precision=12, scale=2), default=0)
    event_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('event.id')
    )
    event: Mapped[Event] = relationship(
        Event,
        foreign_keys=[event_id],
        lazy='joined',
    )
    status = Column(String)
