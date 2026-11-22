from app.pipeline import run_pipeline


def main():
    print("=" * 50)
    print("AI Instagram Lead Finder & Sales Assistant MVP")
    print("=" * 50)

    niche = input("Enter target niche (e.g., 'beauty salon', 'dentist'): ")
    location = input("Enter target location (e.g., 'Baku', 'London'): ")
    use_mock = input("Use mock data for testing? (y/n): ").strip().lower() == "y"

    print(f"\nSearching for '{niche}' in '{location}'...")
    result = run_pipeline(niche, location, use_mock=use_mock)

    if not result["found"]:
        print("No leads found. Try different keywords or check your connection.")
        return

    print(f"Found {result['found']} potential leads.")
    print(f"Saved {result['saved']} NEW leads to the database.")
    print(f"Generated AI sales messages for {result['processed']} leads.")
    print(f"\nDone! Leads exported to: {result['csv_path']}")


if __name__ == "__main__":
    main()
