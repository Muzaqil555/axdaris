import os
from app.scraper import Scraper
from app.analyzer import Analyzer
from app.database import Database
from app.ai_generator import AIGenerator

def main():
    print("="*50)
    print("AI Instagram Lead Finder & Sales Assistant MVP")
    print("="*50)
    
    niche = input("Enter target niche (e.g., 'beauty salon', 'dentist'): ")
    location = input("Enter target location (e.g., 'Baku', 'London'): ")
    
    use_mock_input = input("Use mock data for testing? (y/n): ").lower()
    use_mock = use_mock_input == 'y'

    print(f"\nSearching for '{niche}' in '{location}'...")
    
    # 1. Scrape Leads
    scraper = Scraper(use_mock=use_mock)
    raw_leads = scraper.search_google_for_instagram(niche, location, num_results=20)
    
    if not raw_leads:
        print("No leads found. Try different keywords or check your connection.")
        return
        
    print(f"Found {len(raw_leads)} potential leads.")

    # 2. Analyze & Clean Data
    analyzer = Analyzer()
    processed_leads = analyzer.process_leads(raw_leads, niche)

    # 3. Save to Database
    db = Database()
    new_leads_count = 0
    for lead in processed_leads:
        if db.insert_lead(lead):
            new_leads_count += 1
            
    print(f"Saved {new_leads_count} NEW leads to the database.")

    # 4. Generate AI Sales Data
    unprocessed_leads = db.get_unprocessed_leads()
    if not unprocessed_leads:
        print("No new leads to process with AI.")
    else:
        print(f"\nGenerating AI sales messages for {len(unprocessed_leads)} leads...")
        ai_generator = AIGenerator()
        
        for lead in unprocessed_leads:
            print(f"  -> Processing: {lead['business_name']}")
            ai_data = ai_generator.generate_sales_data(lead)
            
            db.update_lead_ai_data(
                profile_url=lead['profile_url'],
                ai_message=ai_data['message'],
                pain_point=ai_data['pain_point'],
                offer=ai_data['offer']
            )

    # 5. Export to CSV
    csv_path = db.export_to_csv()
    print(f"\nDone! Leads exported to: {csv_path}")

if __name__ == "__main__":
    main()
