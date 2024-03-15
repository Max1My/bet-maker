from sqlalchemy import Column, String

from src.common.mixins.models import PrimaryKeyMixin
from src.db.engine import Base


class Event(Base, PrimaryKeyMixin):
    __tablename__ = "event"
    status = Column(String, nullable=True)
