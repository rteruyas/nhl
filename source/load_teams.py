import csv
import json
import ast
import psycopg2
import yaml
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
CSV_FILE_PATH = OUTPUT_DIR / "teams.csv"
CONFIG_PATH = PROJECT_ROOT / "config.yaml"

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

DB_CONFIG = config["postgres_db"]

def parse_dict_field(value: str) -> str:
    """
    Converts a Python-dict-style string (single quotes) into a proper
    JSON string that Postgres JSONB can accept.
    """
    if not value:
        return None
    parsed = ast.literal_eval(value)  # safely parse the Python dict literal
    return json.dumps(parsed)         # convert to valid JSON string


def load_csv_to_postgres(csv_path: str):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    insert_query = """
        INSERT INTO raw.teams (team_id, raw_data)
        VALUES (%s, %s)
        ON CONFLICT (team_id) DO UPDATE SET
            raw_data = EXCLUDED.raw_data,
            updated_at = now();
    """

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows_to_insert = []

        for row in reader:
            rows_to_insert.append((
                int(row["franchise_id"]), #remapping franchise_id from API to team_id in postgres
                parse_dict_field(row["raw_data"],)
            ))

    try:
        cur.executemany(insert_query, rows_to_insert)
        conn.commit()
        print(f"Inserted/updated {len(rows_to_insert)} rows.")
    except Exception as e:
        conn.rollback()
        print(f"*** Load failed, transaction rolled back: {e}")
        raise  # re-raise so the caller / orchestrator knows this run failed
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    load_csv_to_postgres(CSV_FILE_PATH)