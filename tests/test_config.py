import app.ai_generator as ai_generator
import app.scraper as scraper
from app.config import Config


def test_gemini_model_setting_is_used_by_both_clients(monkeypatch):
    created = []
    monkeypatch.setattr(Config, "GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(Config, "GEMINI_MODEL", "gemini-test-model")
    for module in (scraper, ai_generator):
        monkeypatch.setattr(module.genai, "configure", lambda **_: None)
        monkeypatch.setattr(module.genai, "GenerativeModel", created.append)

    scraper.Scraper()
    ai_generator.AIGenerator()

    assert created == ["gemini-test-model", "gemini-test-model"]
