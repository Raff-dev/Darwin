from fastapi import UploadFile
from pydantic import BaseModel


class DocumentBase(BaseModel):
    filename: str


class DocumentCreate(DocumentBase):
    file: UploadFile


class Document(DocumentBase):
    id: int
