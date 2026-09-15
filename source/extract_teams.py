import csv
import json
from pathlib import Path
from nhlpy.nhl_client import NHLClient

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
CSV_FILE_PATH = OUTPUT_DIR / "teams.csv"

# Make sure the output folder exists before writing to it
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_teams():
    fieldnames = ['franchise_id','raw_data']
    client = NHLClient(debug=False)
    teams = client.teams.teams()
    # Teams for a specific date (useful during preseason)
    # teams = client.teams.teams(date="2024-10-04")

    # Example
    '''
    {'conference': {'abbr': 'W', 'name': 'Western'}, 'division': {'abbr': 'C', 'name': 'Central'},
     'name': 'Colorado Avalanche', 'common_name': 'Avalanche', 'abbr': 'COL',
     'logo': 'https://assets.nhle.com/logos/nhl/svg/COL_light.svg', 'franchise_id': 27}
    '''

    rows = []
    for team in teams:
        rows.append({
            "franchise_id": team["franchise_id"],
            "raw_data": json.dumps(team),
        })

    with (open(CSV_FILE_PATH, "w", newline='', encoding="utf-8")) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
    return teams



def main():
    print("*** Running extract_teams.py")
    load_teams()
    #print(teams)

if __name__ == "__main__":
    main()