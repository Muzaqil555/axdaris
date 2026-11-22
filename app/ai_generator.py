import time
import google.generativeai as genai
from app.config import Config

class AIGenerator:
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        else:
            self.model = None

    def generate_sales_data(self, lead):
        """
        Step 1: Deeply analyzes the business from their Instagram profile.
        Step 2: Figures out which specific automated system would earn them the MOST money.
        Step 3: Writes a hyper-personalized pitch about THAT specific system.
        """
        if not self.model:
            return {
                "best_system": "API açarı tapılmadı",
                "why_this_system": "N/A",
                "message": "Xəta: .env faylında GEMINI_API_KEY tapılmadı.",
                "estimated_revenue": "N/A"
            }

        prompt = f"""
You are a sharp business analyst and elite sales strategist.

A client just found this Instagram business and wants to sell them an automated system.
Your job is NOT to suggest generic services. Your job is to:

1. DEEPLY ANALYZE what this specific business does, how they currently get clients, and where they leak money or time.
2. IDENTIFY the ONE single automated system that would generate the MAXIMUM EXTRA REVENUE for this exact business. Not what's trendy — what FITS THEM.
3. WRITE a short, personalized Instagram DM in Azerbaijani that mentions their specific situation (not generic words) and pitches that one system.

Business Profile:
- Business Name: {lead.get('business_name', 'Unknown')}
- Niche: {lead.get('niche', 'Unknown')}
- Instagram Bio: {lead.get('bio', 'Not available')}
- Followers: {lead.get('follower_estimate', 'Unknown')}
- Contact Info: {lead.get('contact_info', 'Unknown')}
- Profile URL: {lead.get('profile_url', '')}

Your available systems to recommend (pick the BEST ONE that fits):
• AI Appointment Booking Bot — for businesses with manual scheduling (salons, clinics, tutors)
• AI Lead Qualifier + CRM — for businesses where clients ask many questions before buying
• Instagram Auto-DM Follow-up — for businesses with lots of followers but low conversion
• AI Product Recommendation Engine — for e-commerce or product-based businesses
• Loyalty & Repeat-Customer Automation — for businesses where returning customers = big revenue
• AI-Powered Review Collection System — for businesses where reputation drives sales
• WhatsApp Chatbot Sales Funnel — for businesses using WhatsApp as primary contact
• Abandoned Cart / Follow-up Automation — for online stores with many visitors, low buyers

Format your answer EXACTLY like this (no markdown, no extra text):
BEST_SYSTEM:
<Name of the one system you picked>
---
WHY:
<2-3 sentences explaining WHY this specific system fits THIS specific business and how much extra revenue it can generate per month. Be specific and cite numbers if possible.>
---
ESTIMATED_MONTHLY_REVENUE_GAIN:
<A realistic range, e.g. "$500 - $2,000/month extra">
---
MESSAGE:
<The personalized Instagram DM in Azerbaijani. 3-4 sentences max. Mention their name or niche directly. End with a soft call-to-action.>
        """

        try:
            # Retry up to 3 times on rate limit
            for attempt in range(3):
                try:
                    response = self.model.generate_content(prompt)
                    break
                except Exception as e:
                    err_str = str(e)
                    if '429' in err_str and attempt < 2:
                        wait_time = 60 * (attempt + 1)  # 60s, then 120s
                        print(f"Rate limit hit. Waiting {wait_time}s before retry {attempt + 2}/3...")
                        time.sleep(wait_time)
                    else:
                        raise e

            text = response.text.strip()

            parts = text.split('---')
            best_system = ""
            why = ""
            estimated_revenue = ""
            message = ""

            for part in parts:
                p = part.strip()
                if p.startswith("BEST_SYSTEM:"):
                    best_system = p.replace("BEST_SYSTEM:", "").strip()
                elif p.startswith("WHY:"):
                    why = p.replace("WHY:", "").strip()
                elif p.startswith("ESTIMATED_MONTHLY_REVENUE_GAIN:"):
                    estimated_revenue = p.replace("ESTIMATED_MONTHLY_REVENUE_GAIN:", "").strip()
                elif p.startswith("MESSAGE:"):
                    message = p.replace("MESSAGE:", "").strip()

            if not message:
                message = text

            return {
                "best_system": best_system,
                "why_this_system": why,
                "estimated_revenue": estimated_revenue,
                "message": message,
            }

        except Exception as e:
            print(f"Error generating AI content for {lead.get('business_name')}: {e}")
            return {
                "best_system": "Xəta",
                "why_this_system": "N/A",
                "estimated_revenue": "N/A",
                "message": f"Xəta: {str(e)}"
            }
