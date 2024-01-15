import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MEDIA_ROOT = BASE_DIR / "web/media"
STATIC_ROOT = BASE_DIR / "web/static"
TEMPLATES_ROOT = BASE_DIR / "web/templates"

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")

DATABASE_URL = os.getenv("DATABASE_URL", "")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV_NAME = os.getenv("PINECONE_ENV_NAME")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "")
