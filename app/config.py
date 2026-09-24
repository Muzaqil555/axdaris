import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # App Settings
    DB_PATH = os.path.join(os.getcwd(), "data", "leads.db")
    OUTPUT_CSV_PATH = os.path.join(os.getcwd(), "output", "leads.csv")
    
    # Ensure directories exist
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUT_CSV_PATH), exist_ok=True)
