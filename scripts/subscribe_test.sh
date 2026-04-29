#!/bin/bash
set -e

# Load environment variables relative to script location
set -a
source "$(dirname "$0")/../.env"
set +a

mosquitto_sub -h "$MQTT_BROKER" -p "$MQTT_PORT" \
  --cafile "$CA_CERT_PATH" \
  -u "$MQTT_USER" -P "$MQTT_PW" \
  -t "$MQTT_TOPIC"
