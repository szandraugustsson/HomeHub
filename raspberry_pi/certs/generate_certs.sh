#!/bin/bash
set -e

CERT_DIR="$(dirname "$0")"
cd "$CERT_DIR"

# Using hostname recommended instead of IP
HOST="rpi-001.local" # Replace with your Raspberry Pi hostname

echo "Generating CA..."

openssl req -x509 -new -nodes \
  -keyout ca.key \
  -out ca.crt \
  -days 365 \
  -subj "/CN=HomeHub-CA"

echo "Generating server key..."

openssl genrsa -out server.key 2048

echo "Generating CSR..."

openssl req -new \
  -key server.key \
  -out server.csr \
  -subj "/CN=$HOST"

echo "Signing server certificate..."

openssl x509 -req \
  -in server.csr \
  -CA ca.crt \
  -CAkey ca.key \
  -CAcreateserial \
  -out server.crt \
  -days 365

echo "Deploying certificates to Mosquitto..."

sudo mkdir -p /etc/mosquitto/certs

# Copy
sudo cp ca.crt /etc/mosquitto/certs/
sudo cp server.crt /etc/mosquitto/certs/
sudo cp server.key /etc/mosquitto/certs/

# Secure permissions
sudo chown mosquitto:mosquitto /etc/mosquitto/certs/*
sudo chmod 600 /etc/mosquitto/certs/server.key
sudo chmod 644 /etc/mosquitto/certs/ca.crt /etc/mosquitto/certs/server.crt

echo "Done"
echo "Certificates generated and deployed to Mosquitto"
