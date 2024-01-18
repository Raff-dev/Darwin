from typing import Any

from sqlalchemy import Column
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Integer, String

from darwin.web.database import Base
from darwin.web.utils import MembershipEnum


class Status(MembershipEnum):
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
