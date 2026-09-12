import csv
from pathlib import Path
from nhlpy.nhl_client import NHLClient

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
CSV_FILE_PATH = OUTPUT_DIR / "teams.csv"

# Make sure the output folder exists before writing to it
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_teams():
    fieldnames = ['conference', 'division', 'name', 'common_name','abbr','logo','franchise_id']
    client = NHLClient(debug=False)
    teams = client.teams.teams()
    # Teams for a specific date (useful during preseason)
    # teams = client.teams.teams(date="2024-10-04")
    with (open(CSV_FILE_PATH, "w", newline='', encoding="utf-8")) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(teams)
    return teams

def main():
    print("*** Running extract_teams.py")
    load_teams()
    #print(teams)

if __name__ == "__main__":
    main()