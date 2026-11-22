import pandas as pd

from app.database import Database
from app.pipeline import run_pipeline


class FakeAI:
    def __init__(self):
        self.calls = 0

    def generate_sales_data(self, lead):
        self.calls += 1
        return {
            "best_system": "AI Appointment Booking Bot",
            "why_this_system": "Manual booking via DM.",
            "estimated_revenue": "$500 - $1,000/month extra",
            "message": f"Salam, {lead['business_name']}!",
        }


def make_db(tmp_path):
    return Database(db_path=str(tmp_path / "leads.db"), csv_path=str(tmp_path / "leads.csv"))


def test_run_pipeline_with_mock_data_saves_and_processes_leads(tmp_path):
    db = make_db(tmp_path)
    ai = FakeAI()

    result = run_pipeline("beauty salon", "Baku", use_mock=True, db=db,
                          ai_generator=ai, delay_seconds=0, log=lambda *_: None)

    assert result["found"] == 2
    assert result["saved"] == 2
    assert result["processed"] == 2
    assert ai.calls == 2
    leads = db.get_all_leads()
    assert all(lead["status"] == "processed" for lead in leads)
    assert all(lead["best_system"] == "AI Appointment Booking Bot" for lead in leads)
    assert len(pd.read_csv(result["csv_path"])) == 2


def test_second_run_does_not_duplicate_or_reprocess(tmp_path):
    db = make_db(tmp_path)
    kwargs = dict(use_mock=True, db=db, delay_seconds=0, log=lambda *_: None)
    run_pipeline("beauty salon", "Baku", ai_generator=FakeAI(), **kwargs)

    ai = FakeAI()
    result = run_pipeline("beauty salon", "Baku", ai_generator=ai, **kwargs)

    assert result["saved"] == 0
    assert ai.calls == 0
    assert len(db.get_all_leads()) == 2


def test_leads_endpoint_returns_saved_leads(tmp_path, monkeypatch):
    from fastapi.testclient import TestClient

    import server
    from app.config import Config

    monkeypatch.setattr(Config, "DB_PATH", str(tmp_path / "leads.db"))
    db = Database()
    db.insert_lead({"business_name": "Test", "niche": "salon",
                    "profile_url": "https://www.instagram.com/test/"})

    response = TestClient(server.app).get("/api/leads")

    assert response.status_code == 200
    assert [lead["business_name"] for lead in response.json()["leads"]] == ["Test"]
