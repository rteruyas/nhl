CREATE SCHEMA raw;

CREATE TABLE raw.teams (
    team_id  				INTEGER,
    raw_data    			JSONB NOT NULL,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (team_id)
);


CREATE TABLE raw.players (
    id                      INTEGER,       				-- NHL player id
    team_id            		INTEGER,
    season					INTEGER,
    position_group          TEXT NOT NULL, 			   	--('forwards', 'defensemen', 'goalies')
    raw_data	            JSONB NOT NULL,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (id, team_id, season)
);