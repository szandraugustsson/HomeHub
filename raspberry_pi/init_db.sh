#!/bin/bash
# Initialize SQLite database with telemetry table and timestamp index

DB_FILE="sensor_data.db"

echo "Initializing SQLite database at $DB_FILE..."

sqlite3 "$DB_FILE" <<EOF
CREATE TABLE IF NOT EXISTS telemetry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    topic TEXT NOT NULL,
    value REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_timestamp ON telemetry(timestamp);
EOF

echo "Database initialization complete."
