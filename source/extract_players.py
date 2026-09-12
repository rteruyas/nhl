import csv
import json
from pathlib import Path
from nhlpy.nhl_client import NHLClient

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
CSV_FILE_PATH = OUTPUT_DIR / "players.csv"
SEASON = "20252026"

# Make sure the output folder exists before writing to it
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_players():
    fieldnames = ["id", "franchise_id", "season", "position_group", "raw_data"]
    client = NHLClient(debug=False)
    client = NHLClient(debug=False)
    teams = client.teams.teams()
    # teams = client.teams.teams(date="2024-10-04")

    # Example
    '''
    {'conference': {'abbr': 'W', 'name': 'Western'}, 'division': {'abbr': 'C', 'name': 'Central'},
     'name': 'Colorado Avalanche', 'common_name': 'Avalanche', 'abbr': 'COL',
     'logo': 'https://assets.nhle.com/logos/nhl/svg/COL_light.svg', 'franchise_id': 27}
    '''

    rows = []
    for team in teams:
        players = client.teams.team_roster(team_abbr=team["abbr"], season=SEASON)
        for position_group, players in players.items():
            for player in players:
                rows.append({
                    "id": player["id"],
                    "franchise_id": team["franchise_id"],
                    "season": SEASON,
                    "position_group": position_group,
                    "raw_data": json.dumps(player),  # entire object, untouched
                })
    with (open(CSV_FILE_PATH, "w", newline='', encoding="utf-8")) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
    return players

def main():
    print("*** Running extract_players.py")
    players = load_players()

if __name__ == "__main__":
    main()