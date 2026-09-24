from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import time
from app.scraper import Scraper
from app.analyzer import Analyzer
from app.database import Database
from app.ai_generator import AIGenerator

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
    scraper = Scraper(use_mock=use_mock)
    raw_leads = scraper.search_google_for_instagram(niche, location, num_results=20)
    
    if not raw_leads:
        return

    analyzer = Analyzer()
    processed_leads = analyzer.process_leads(raw_leads, niche)

    db = Database()
    for lead in processed_leads:
        db.insert_lead(lead)

    unprocessed_leads = db.get_unprocessed_leads()
    if unprocessed_leads:
        ai_generator = AIGenerator()
        for i, lead in enumerate(unprocessed_leads):
            print(f"AI analyzing lead {i+1}/{len(unprocessed_leads)}: {lead.get('business_name')}")
            ai_data = ai_generator.generate_sales_data(lead)
            db.update_lead_ai_data(
                profile_url=lead['profile_url'],
                ai_message=ai_data.get('message', ''),
                best_system=ai_data.get('best_system', ''),
                why_this_system=ai_data.get('why_this_system', ''),
                estimated_revenue=ai_data.get('estimated_revenue', '')
            )
            # Small delay between API calls to respect rate limits
            if i < len(unprocessed_leads) - 1:
                time.sleep(4)
    
    db.export_to_csv()

@app.post("/api/search")
async def start_search(request: SearchRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_leads_task, request.niche, request.location, request.use_mock)
    return {"status": "started", "message": "Search and AI generation started in the background."}

@app.get("/api/leads")
async def get_leads():
    db = Database()
    with db.get_connection() as conn:
        conn.row_factory = import_sqlite3_row(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM leads ORDER BY id DESC")
        leads = [dict(row) for row in cursor.fetchall()]
    return {"leads": leads}

def import_sqlite3_row(conn):
    import sqlite3
    return sqlite3.Row

# Serve index.html at root
from fastapi.responses import FileResponse
@app.get("/")
async def read_index():
    return FileResponse("static/index.html")
