import os

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from web.api.documents.crud import router as documents_router
from web.settings import STATIC_ROOT, TEMPLATES_ROOT

app = FastAPI()
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=STATIC_ROOT), name=str(STATIC_ROOT))
templates = Jinja2Templates(directory=TEMPLATES_ROOT)

api_router = APIRouter()


@app.get("/")
def redirect_to_api_root(_: Request):
    return RedirectResponse(url="/api")


@api_router.get("/")
def root(_: Request):
    return [route.path for route in app.router.routes if isinstance(route, Route)]


api_router.include_router(documents_router, prefix="/documents", tags=["documents"])
app.include_router(api_router, prefix="/api")
