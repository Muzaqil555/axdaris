import pytest

from app.scraper import Scraper, parse_leads_json

LEAD = '{"business_name": "Glow", "profile_url": "https://www.instagram.com/glow/"}'


@pytest.mark.parametrize("text", [
    f"[{LEAD}]",
    f"```json\n[{LEAD}]\n```",
    f"```JSON\n[{LEAD}]\n```\n",
    f"Here are the accounts I found:\n```\n[{LEAD}]\n```\nLet me know if you need more.",
    f"Sure! [{LEAD}] Hope this helps.",
    f'{{"leads": [{LEAD}]}}',
    f"  \n[{LEAD}]\n  ",
])
def test_parses_common_model_output_shapes(text):
    leads = parse_leads_json(text)
    assert leads == [{"business_name": "Glow", "profile_url": "https://www.instagram.com/glow/"}]


def test_skips_bracketed_prose_before_the_array():
    text = f"[Note] I could only find one account: [{LEAD}]"
    assert parse_leads_json(text)[0]["business_name"] == "Glow"


def test_drops_non_object_items():
    assert parse_leads_json(f'[{LEAD}, "oops", 3]') == [parse_leads_json(f"[{LEAD}]")[0]]


def test_empty_array_is_valid():
    assert parse_leads_json("[]") == []


@pytest.mark.parametrize("text", ["", "   ", "I couldn't find any accounts.", "[1, 2, 3]", '{"error": "x"}'])
def test_unusable_output_raises(text):
    with pytest.raises(ValueError):
        parse_leads_json(text)


class _FakeModel:
    def __init__(self, text):
        self.text = text

    def generate_content(self, prompt):
        return self


def test_scraper_uses_parser_and_deduplicates():
    s = Scraper(use_mock=True)
    s.use_mock = False
    s.model = _FakeModel(f"Here you go:\n```json\n[{LEAD}, {LEAD}]\n```")
    assert len(s.search_google_for_instagram("salon", "Baku")) == 1


def test_scraper_falls_back_to_mock_on_garbage():
    s = Scraper(use_mock=True)
    s.use_mock = False
    s.model = _FakeModel("Sorry, I can't help with that.")
    leads = s.search_google_for_instagram("salon", "Baku")
    assert leads and "Glow" in leads[0]["business_name"]
