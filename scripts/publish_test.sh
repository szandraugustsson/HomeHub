#!/bin/bash
set -e

# Load environment variables relative to script location
set -a
source "$(dirname "$0")/../.env"
set +a

mosquitto_pub -h "$MQTT_BROKER" -p "$MQTT_PORT" \
  --cafile "$CA_CERT_PATH" \
  -u "$MQTT_USER" -P "$MQTT_PW" \
  -t sensors/temp -m "-2.2"

mosquitto_pub -h "$MQTT_BROKER" -p "$MQTT_PORT" \
  --cafile "$CA_CERT_PATH" \
  -u "$MQTT_USER" -P "$MQTT_PW" \
  -t sensors/humidity -m "45.5"
