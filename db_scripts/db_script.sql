CREATE SCHEMA raw;

CREATE TABLE raw.teams (
    team_id  INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    common_name   TEXT NOT NULL,
    abbr          TEXT NOT NULL,
    logo          TEXT,
    conference    JSONB NOT NULL,  -- e.g. {"abbr": "W", "name": "Western"}
    division      JSONB NOT NULL   -- e.g. {"abbr": "C", "name": "Central"}
);


CREATE TABLE raw.players (
    id                      INTEGER,       				-- NHL player id
    team_id                 INTEGER,
    season					INTEGER,
    position_group          TEXT NOT NULL, 			   	--('forwards', 'defensemen', 'goalies')
    raw_data	            JSONB NOT NULL,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (id, team_id, season)
);

