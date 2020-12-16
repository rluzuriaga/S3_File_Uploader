CREATE TABLE IF NOT EXISTS versioning (
    db_version INTEGER NOT NULL
);

DELETE FROM versioning;

INSERT INTO versioning (db_version) VALUES (2);