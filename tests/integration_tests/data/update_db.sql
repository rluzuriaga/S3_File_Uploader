-- SQL file used to test that the UpdateDatabase window is working

CREATE TABLE IF NOT EXISTS tests (
    test_column TEXT NOT NULL
);

INSERT INTO tests (test_column) VALUES ("This is a test.");