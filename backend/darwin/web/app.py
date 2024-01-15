from darwin.web.api.conversations.crud import router as conversations_router
from darwin.web.api.documents.crud import router as documents_router
from darwin.web.database import Base, engine
from darwin.web.settings import ALLOWED_ORIGINS, STATIC_ROOT, TEMPLATES_ROOT
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()
router = APIRouter()


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=STATIC_ROOT), name=str(STATIC_ROOT))
templates = Jinja2Templates(directory=TEMPLATES_ROOT)


@app.get("/")
def redirect_to_api_root(_: Request):
    return RedirectResponse(url="/api")


@router.get("/")
def root(_: Request):
    return [route.path for route in app.router.routes if isinstance(route, Route)]


router.include_router(documents_router, prefix="/documents", tags=["documents"])
router.include_router(
    conversations_router, prefix="/conversations", tags=["conversations"]
)
app.include_router(router, prefix="/api")

Base.metadata.create_all(bind=engine)
