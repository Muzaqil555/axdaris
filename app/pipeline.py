import time

from app.analyzer import Analyzer
from app.database import Database
from app.scraper import Scraper


def find_and_save_leads(niche, location, use_mock=False, num_results=20, db=None):
    """Finds leads, cleans them and saves the new ones. Returns (found, saved)."""
    db = db or Database()
    raw_leads = Scraper(use_mock=use_mock).search_google_for_instagram(
        niche, location, num_results=num_results
    )
    if not raw_leads:
        return 0, 0

    processed = Analyzer().process_leads(raw_leads, niche)
    saved = sum(1 for lead in processed if db.insert_lead(lead))
    return len(raw_leads), saved


def generate_ai_for_new_leads(db=None, ai_generator=None, delay_seconds=4, log=print):
    """Runs the AI on every lead that has not been processed yet. Returns the count."""
    db = db or Database()
    leads = db.get_unprocessed_leads()
    if not leads:
        return 0

    if ai_generator is None:
        from app.ai_generator import AIGenerator
        ai_generator = AIGenerator()

    for i, lead in enumerate(leads):
        log(f"AI analyzing lead {i + 1}/{len(leads)}: {lead.get('business_name')}")
        ai_data = ai_generator.generate_sales_data(lead)
        db.update_lead_ai_data(
            profile_url=lead["profile_url"],
            ai_message=ai_data.get("message", ""),
            best_system=ai_data.get("best_system", ""),
            why_this_system=ai_data.get("why_this_system", ""),
            estimated_revenue=ai_data.get("estimated_revenue", ""),
        )
        # Small delay between API calls to respect rate limits
        if delay_seconds and i < len(leads) - 1:
            time.sleep(delay_seconds)
    return len(leads)


def run_pipeline(niche, location, use_mock=False, db=None, ai_generator=None,
                 delay_seconds=4, log=print):
    """Full run: find leads, generate AI messages, export CSV. Returns a summary dict."""
    db = db or Database()
    found, saved = find_and_save_leads(niche, location, use_mock=use_mock, db=db)
    processed = 0
    if found:
        processed = generate_ai_for_new_leads(
            db=db, ai_generator=ai_generator, delay_seconds=delay_seconds, log=log
        )
    csv_path = db.export_to_csv()
    return {"found": found, "saved": saved, "processed": processed, "csv_path": csv_path}
