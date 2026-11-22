import os

from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.database import Database
from app.pipeline import run_pipeline

app = FastAPI()

# Make sure static folder exists
os.makedirs("static", exist_ok=True)

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")


class SearchRequest(BaseModel):
    niche: str
    location: str
    use_mock: bool = False


def process_leads_task(niche: str, location: str, use_mock: bool):
    run_pipeline(niche, location, use_mock=use_mock)


@app.post("/api/search")
async def start_search(request: SearchRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_leads_task, request.niche, request.location, request.use_mock)
    return {"status": "started", "message": "Search and AI generation started in the background."}


@app.get("/api/leads")
async def get_leads():
    return {"leads": Database().get_all_leads()}


# Serve index.html at root
@app.get("/")
async def read_index():
    return FileResponse("static/index.html")
