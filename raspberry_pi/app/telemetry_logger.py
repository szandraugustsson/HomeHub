import os
import ssl
import sqlite3
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Default values here are just placeholders and should be replaced in your local .env
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_USER = os.getenv("MQTT_USER", "your_user")
MQTT_PW = os.getenv("MQTT_PW", "your_password")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "your_topic")
CA_CERT = os.path.abspath(os.getenv("CA_CERT_PATH", "raspberry_pi/certs/ca.crt"))
DB_PATH = os.getenv("DB_PATH", "your_path_to_database")

# Setup SQLite
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode("utf-8").strip()
        value = float(payload_str)
        cursor.execute("INSERT INTO telemetry (topic, value) VALUES (?, ?)", (msg.topic, value))
        conn.commit()
        print(f"Saved: {msg.topic} -> {value}")
    except Exception as e:
        print(f"Error: {e}")

# Setup MQTT client
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PW)
client.on_message = on_message

# TLS
client.tls_set(
    ca_certs=CA_CERT,
    certfile=None,
    keyfile=None,
    tls_version=ssl.PROTOCOL_TLS_CLIENT,
)
client.tls_insecure_set(False)

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.subscribe(MQTT_TOPIC)
    print(f"Connected to {MQTT_BROKER}:{MQTT_PORT}, subscribing to {MQTT_TOPIC}")
    client.loop_forever()
except KeyboardInterrupt:
    print("Exiting and closing the database...")
    conn.close()
except Exception as e:
    print(f"Error connecting to MQTT: {e}")
    conn.close()
