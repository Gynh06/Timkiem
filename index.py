from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

OUTPUT_FILE = "output.txt"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/find")
async def find_keyword(
    file: UploadFile,
    keyword: str = Form(...)
):
    keyword = keyword.lower()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break

            lines = chunk.decode("utf-8", errors="ignore").splitlines()
            for line in lines:
                if keyword in line.lower():
                    out.write(line + "\n")

    return FileResponse(
        OUTPUT_FILE,
        filename="output.txt",
        media_type="text/plain"
    )