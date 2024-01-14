import os
import uuid
from pathlib import Path

from fastapi import APIRouter, FastAPI, File, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, RedirectResponse
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
MEDIA_ROOT = BASE_DIR / "media"
STATIC_ROOT = BASE_DIR / "static"
TEMPLATES_ROOT = BASE_DIR / "templates"

app = FastAPI()
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

print(allowed_origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=STATIC_ROOT), name=str(STATIC_ROOT))
templates = Jinja2Templates(directory=TEMPLATES_ROOT)

router = APIRouter()


@app.get("/")
def redirect_to_api(_: Request):
    return RedirectResponse(url="/api")


@router.get("/")
def root(_: Request):
    return [route.path for route in app.router.routes if isinstance(route, Route)]


@router.post("/documents")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return JSONResponse(
            status_code=400, content={"error": "Only PDF files are allowed."}
        )

    filename = uuid.uuid4()
    with open(f"{MEDIA_ROOT}/{filename}", "wb") as buffer:
        buffer.write(await file.read())

    return {"filename": filename}


@router.get("/hello")
def hello(_: Request):
    return {"message": "Hello World!"}


app.include_router(router, prefix="/api")
