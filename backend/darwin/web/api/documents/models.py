from enum import Enum
from typing import Any

from darwin.web.database import Base
from sqlalchemy import Column
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Integer, String


class Status(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    ERROR = "error"


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(100), nullable=False)
    filepath = Column(String(100), nullable=False)
    status: Any = Column(SqlEnum(Status), default=Status.PENDING)
