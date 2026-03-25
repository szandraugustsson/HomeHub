#!/bin/bash
# Delete telemetry-data older than 7 days
sqlite3 ~/HomeHub/raspberry_pi/sensor_data.db \
"DELETE FROM telemetry WHERE timestamp < datetime('now', '-7 days');"
