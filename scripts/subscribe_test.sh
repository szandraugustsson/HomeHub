#!/bin/bash
# Load environment variables from .env
set -a
source "$HOME/HomeHub/.env"
set +a

mosquitto_sub -h $MQTT_BROKER -p $MQTT_PORT \
  --cafile $CA_CERT_PATH \
  -u $MQTT_USER -P $MQTT_PW \
  -t $MQTT_TOPIC
