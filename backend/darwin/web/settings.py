import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MEDIA_ROOT = BASE_DIR / "media"
STATIC_ROOT = BASE_DIR / "static"
TEMPLATES_ROOT = BASE_DIR / "templates"

DATABASE_URL = os.getenv("DATABASE_URL", "")
