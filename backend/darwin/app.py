from pathlib import Path

from fastapi import FastAPI, File, Request, UploadFile
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
MEDIA_ROOT = BASE_DIR / "media"
STATIC_ROOT = BASE_DIR / "static"
TEMPLATES_ROOT = BASE_DIR / "templates"

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_ROOT), name=str(STATIC_ROOT))
templates = Jinja2Templates(directory=TEMPLATES_ROOT)


@app.get("/")
def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return JSONResponse(
            status_code=400, content={"error": "Only PDF files are allowed."}
        )

    with open(f"{MEDIA_ROOT}/{file.filename}", "wb") as buffer:
        buffer.write(await file.read())

    return {"filename": file.filename}
