import os
import ssl
import sqlite3
import requests
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USER = os.getenv("MQTT_USER", "your_user")
MQTT_PW = os.getenv("MQTT_PW", "your_password")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "sensors/#")

CA_CERT = os.path.abspath(
    os.getenv("CA_CERT_PATH", "/etc/mosquitto/certs/ca.crt")
)

DB_PATH = os.getenv("DB_PATH", "./raspberry_pi/sensor_data.db")

TB_TOKEN = os.getenv("THINGSBOARD_TOKEN", "your_fallback_token")
tb_url = f"https://thingsboard.cloud/api/v1/{TB_TOKEN}/telemetry"

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

def on_connect(client, userdata, flags, rc):
    print("MQTT CONNECTED", rc)
    client.subscribe(MQTT_TOPIC)

def on_disconnect(client, userdata, rc):
    print("MQTT DISCONNECTED", rc)

def on_message(client, userdata, msg):
    print("MQTT RECEIVED:", msg.topic, msg.payload)
    try:
        payload_str = msg.payload.decode("utf-8").strip()
        try:
            value = float(payload_str)
        except ValueError:
            print(f"Invalid payload: {payload_str}")
            return

        if value == -127.0 or value == 127.0:
            print("Ignored sensor error value")
            return

        cursor.execute(
            "INSERT INTO telemetry (topic, value) VALUES (?, ?)",
            (msg.topic, value)
        )
        conn.commit()
        print(f"Saved: {msg.topic} -> {value}")

        cloud_key = msg.topic.replace("/", "_")
        cloud_payload = {cloud_key: value, "status": "SECURE"}

        response = requests.post(tb_url, json=cloud_payload, timeout=5)

        if response.status_code == 200:
            print("Saved to cloud")
        else:
            print(f"Cloud Sync failed: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")

client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PW)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.reconnect_delay_set(min_delay=1, max_delay=10)

client.tls_set(
    ca_certs=CA_CERT,
    tls_version=ssl.PROTOCOL_TLS_CLIENT,
)

client.tls_insecure_set(False)

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print(f"Connected to {MQTT_BROKER}:{MQTT_PORT}, subscribing to {MQTT_TOPIC}")
    client.loop_forever()

except KeyboardInterrupt:
    print("Exiting and closing database...")
    conn.close()

except Exception as e:
    print(f"Error connecting to MQTT: {e}")
    conn.close()
