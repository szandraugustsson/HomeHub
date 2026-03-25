# Home Hub – Raspberry Pi Zero / MQTT / SQLite / TLS

This is the Raspberry Pi Zero part of the **Home Hub** project.  
It handles **data storage** from **MQTT** messages, saving them locally to **SQLite**, and supports **TLS encryption**.

---

## Project Overview

1. ESP32 sends sensor data to the Raspberry Pi Zero via MQTT.  
2. Python program receives the data.  
3. The Python program:
   - Saves the data locally in `sensor_data.db` (backup in case of internet loss)  
   - Sends data to ThingsBoard over the internet *(not yet implemented)*

---

## Installation

On Raspberry Pi Zero:

sudo apt update
sudo apt install -y mosquitto mosquitto-clients sqlite3 python3-pip

---

### Python Virtual Environment (venv)

1. Navigate to the project folder:
cd ~/HomeHub

2. Create a Python virtual environment:
python3 -m venv venv

3. Activate the virtual environment:
source venv/bin/activate

- Your prompt should now show `(venv)` to indicate the environment is active.

4. Install the required Python packages:

pip install --upgrade pip
pip install -r requirements.txt

## Configuration (.env)

1. Copy the example environment file:
cp .env.example .env

2. Fill in your own MQTT credentials and paths in `.env`:

MQTT_BROKER=localhost
MQTT_PORT=8883
MQTT_USER=your_user
MQTT_PASS=your_password
MQTT_TOPIC=sensors/#
CA_CERT_PATH=your_path
DB_PATH=raspberry_pi/sensor_data.db

3. **Do not commit `.env` to GitHub.**
---
## TLS / Self-Signed Certificates
Generate certificates (if not already):

./raspberry_pi/certs/generate_certs.sh

Add the CA certificate to the system’s trusted certificates:
sudo cp raspberry_pi/certs/ca.crt /usr/local/share/ca-certificates/ca_homehub.crt
sudo update-ca-certificates
In the logger, TLS should be configured like this:
client.tls_set(
    ca_certs=CA_CERT,
    certfile=None,
    keyfile=None,
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)
client.tls_insecure_set(False)  # safe since CA is trusted

Do not set tls_insecure_set(True) in production, it disables certificate verification.
---



## MQTT Configuration

### 1. Copy config file

sudo cp raspberry_pi/mqtt_setup/mosquitto_conf_example.conf /etc/mosquitto/conf.d/external.conf
## CONFIGURE MOSQUITO HÄR ISTÄLLET!!

### 2. Create user/password

sudo mosquitto_passwd -c /etc/mosquitto/passwd sensoruser

### 3. Set permissions
sudo chown mosquitto:mosquitto /etc/mosquitto/passwd
sudo chmod 600 /etc/mosquitto/passwd

### 4. Restart Mosquitto
sudo systemctl restart mosquitto

**Note:**  
- Replace TLS certificate paths in the config if needed  
- For local testing only, you can set `allow_anonymous true`


## Configure Mosquitto
Edit /etc/mosquitto/conf.d/external.conf:

listener 8883
allow_anonymous false
password_file /etc/mosquitto/passwd

cafile /etc/mosquitto/certs/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key

---

## Initialize SQLite Database
cd raspberry_pi
./init_db.sh

This creates `sensor_data.db` with a `telemetry` table containing:

- `id` – unique identifier  
- `timestamp` – automatically recorded datetime  
- `topic` – sensor name (e.g. `sensors/temperature`)  
- `value` – numeric sensor reading  

---

## Run the Python Logger

<<<<<<< HEAD
=======
You have two ways to run the logger:

### 1. Manual (for testing or development)

```bash
>>>>>>> 3f9005d (Update README.md)
source venv/bin/activate
python3 raspberry_pi/app/telemetry_logger.py

This script will:

- Connect to the local MQTT broker  
- Subscribe to `sensors/#` topics  
- Save incoming messages to the database  
- Print received values to the terminal

Deactivate the virtual environment when done:
deactivate
<<<<<<< HEAD

---

## Testing

### Publish Example Data
./scripts/publish_test.sh

### Subscribe and View Data

./scripts/subscribe_test.sh

### View database contents

sqlite3 sensor_data.db "SELECT * FROM telemetry;"

---

## Cleanup Script (Optional)

To keep the SQLite database from growing indefinitely:

1. Create `cleanup.sh`:

nano cleanup.sh


Paste:

#!/bin/bash
sqlite3 raspberry_pi/sensor_data.db
"DELETE FROM telemetry WHERE timestamp < datetime('now', '-7 days');"


2. Make it executable:

chmod +x cleanup.sh


3. Schedule with cron (runs daily at 3 AM):

crontab -e

1

Add:
0 3 * * * /home/pi/HomeHub/cleanup.sh

---

## TLS Certificate Generation (Important)

1. Create script:

nano raspberry_pi/certs/generate_certs.sh

Paste:

#!/bin/bash
mkdir -p raspberry_pi/certs
cd raspberry_pi/certs

CA

openssl genrsa -out ca.key 2048
openssl req -x509 -new -nodes -key ca.key -days 365 -out ca.crt

Server

openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key
-CAcreateserial -out server.crt -days 365

echo "Certificates generated"


2. Make it executable:
chmod +x raspberry_pi/certs/generate_certs.sh

3. Run it:

./raspberry_pi/certs/generate_certs.sh

Copy the certificates to Mosquitto and set permissions:

sudo mkdir -p /etc/mosquitto/certs
sudo cp raspberry_pi/certs/*.crt /etc/mosquitto/certs/
sudo cp raspberry_pi/certs/*.key /etc/mosquitto/certs/
sudo chown mosquitto:mosquitto /etc/mosquitto/certs/*
sudo chmod 600 /etc/mosquitto/certs/*
---

## MQTT TLS Setup

- Certificates are stored in `raspberry_pi/certs/`  
- Use port **8883** (TLS) instead of **1883**  
- Python script is already configured for TLS  

---

## Systemd Auto-Start
=======
```
### 2. Automatic (recommended) - Systemd Auto-Start
>>>>>>> 3f9005d (Update README.md)

A systemd service runs the logger automatically:

1. Create a service file:
<<<<<<< HEAD

sudo nano /etc/systemd/system/homehub.service

2. Paste the following:

=======
```bash
sudo vim /etc/systemd/system/homehub.service
```
2. Paste the following:
```bash
>>>>>>> 3f9005d (Update README.md)
[Unit]
Description=HomeHub Telemetry Logger
After=network.target

[Service]
Type=simple
User=dev
WorkingDirectory=/home/dev/HomeHub
ExecStart=/home/dev/HomeHub/venv/bin/python3 /home/dev/HomeHub/raspberry_pi/app/telemetry_logger.py
Restart=always

[Install]
WantedBy=multi-user.target
<<<<<<< HEAD

3. Enable and start the service:

sudo systemctl daemon-reload
sudo systemctl enable homehub.service
sudo systemctl start homehub.service

4. Check status:

=======
```
3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable homehub.service
sudo systemctl start homehub.service
```
4. Check status:
```bash
>>>>>>> 3f9005d (Update README.md)
sudo systemctl status homehub.service

---

## Notes

- Keep TLS private keys out of GitHub (`.gitignore` handles this)  
- Use `tmux` or multiple terminals to run scripts simultaneously  
- This project is for educational purposes


## Data Format

- Topic: `sensors/temperature`  
- Payload: `22.2`
