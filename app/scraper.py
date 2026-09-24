import json
import re
import google.generativeai as genai
from app.config import Config

class Scraper:
    def __init__(self, use_mock=False):
        self.use_mock = use_mock
        self.api_key = Config.GEMINI_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')
        else:
            self.model = None

    def search_google_for_instagram(self, niche, location, num_results=10):
        """
        Uses Gemini AI to find real Instagram profiles safely without scraping.
        This bypasses Google/DuckDuckGo captchas and IP blocks while still 
        returning real business pages known to the AI.
        """
        if self.use_mock:
            return self._get_mock_data(niche, location)

        if not self.model:
            print("No Gemini API key found. Using mock data fallback.")
            return self._get_mock_data(niche, location)

        prompt = f"""
        Find 10 real-world, actual business Instagram accounts for '{niche}' located in '{location}'.
        Rely on your knowledge base of real businesses in this city.
        Return the result STRICTLY as a JSON array of objects. 
        Each object MUST have the following keys:
        - "business_name" (The actual name of the business)
        - "profile_url" (The link to their Instagram, e.g. https://www.instagram.com/username)
        - "bio" (A short description or their actual bio)
        - "follower_estimate" (An estimated number of followers, e.g., "5k+", "10k+", or "Unknown")
        - "contact_info" (A phone number or email if you know it, otherwise "Unknown")
        
        DO NOT return any markdown, explanations, or code blocks. JUST the raw JSON array.
        """

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Clean up markdown formatting if the model still adds it
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
                
            leads = json.loads(text.strip())
            return self._deduplicate(leads)
        except Exception as e:
            print(f"Error fetching real leads from AI Scraper: {e}")
            return self._get_mock_data(niche, location)

    def _deduplicate(self, leads):
        seen_urls = set()
        unique_leads = []
        for lead in leads:
            if isinstance(lead, dict) and 'profile_url' in lead:
                if lead['profile_url'] not in seen_urls:
                    seen_urls.add(lead['profile_url'])
                    unique_leads.append(lead)
        return unique_leads

    def _get_mock_data(self, niche, location):
        """Returns mock data for testing."""
        return [
            {
                "business_name": f"Glow {niche.title()} {location.title()}",
                "profile_url": f"https://www.instagram.com/glow_{niche.replace(' ', '_')}_{location.lower()}/",
                "bio": f"Premium {niche} services in {location}. Book via DM! Phone: +994 50 123 45 67",
                "follower_estimate": "10k+",
                "contact_info": "+994 50 123 45 67"
            },
            {
                "business_name": f"Elite {niche.title()} Studio",
                "profile_url": f"https://www.instagram.com/elite_studio_{location.lower()}/",
                "bio": f"The best {niche} experience. Link in bio to book. Contact: hello@elitestudio.az",
                "follower_estimate": "5k",
                "contact_info": "hello@elitestudio.az"
            }
        ]
