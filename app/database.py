import sqlite3
import pandas as pd
from app.config import Config

class Database:
    def __init__(self):
        self.db_path = Config.DB_PATH
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    business_name TEXT,
                    niche TEXT,
                    profile_url TEXT UNIQUE,
                    bio TEXT,
                    follower_estimate TEXT,
                    contact_info TEXT,
                    ai_message TEXT,
                    best_system TEXT,
                    why_this_system TEXT,
                    estimated_revenue TEXT,
                    status TEXT DEFAULT 'new'
                )
            ''')
            # Add new columns if they don't exist yet (for existing databases)
            for col in ['best_system', 'why_this_system', 'estimated_revenue']:
                try:
                    cursor.execute(f'ALTER TABLE leads ADD COLUMN {col} TEXT')
                except Exception:
                    pass
            conn.commit()

    def insert_lead(self, lead_data):
        """
        Inserts a lead into the database. Ignores if profile_url already exists.
        lead_data: dict with keys matching the columns.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO leads (business_name, niche, profile_url, bio, follower_estimate, contact_info)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    lead_data.get('business_name', ''),
                    lead_data.get('niche', ''),
                    lead_data.get('profile_url', ''),
                    lead_data.get('bio', ''),
                    lead_data.get('follower_estimate', ''),
                    lead_data.get('contact_info', '')
                ))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                # URL already exists
                return False

    def update_lead_ai_data(self, profile_url, ai_message, best_system, why_this_system, estimated_revenue):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE leads 
                SET ai_message = ?, best_system = ?, why_this_system = ?, estimated_revenue = ?, status = 'processed'
                WHERE profile_url = ?
            ''', (ai_message, best_system, why_this_system, estimated_revenue, profile_url))
            conn.commit()

    def get_unprocessed_leads(self):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM leads WHERE status = 'new'")
            return [dict(row) for row in cursor.fetchall()]
            
    def export_to_csv(self):
        with self.get_connection() as conn:
            df = pd.read_sql_query("SELECT * FROM leads", conn)
            df.to_csv(Config.OUTPUT_CSV_PATH, index=False, encoding='utf-8')
            return Config.OUTPUT_CSV_PATH
