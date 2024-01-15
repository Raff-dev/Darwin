from sqlalchemy import Column, Integer, String

from darwin.web.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(100), nullable=False)
    filepath = Column(String(100), nullable=False)
