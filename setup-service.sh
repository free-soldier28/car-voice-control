#!/bin/bash
set -e

echo "=============================================="
echo "?? Setting up car-voice-control Python service"
echo "=============================================="

# === CONFIGURATION ===
SERVICE_NAME="car-voice-control"
APP_DIR="/opt/car-voice-control"
PYTHON_BIN="$APP_DIR/venv/bin/python"
REQUIREMENTS="$APP_DIR/requirements.txt"
MAIN_SCRIPT="$APP_DIR/main.py"
LOG_FILE="/var/log/car-voice.log"
USER_NAME="root"

# === CREATE VENV AND INSTALL DEPENDENCIES ===
echo "1. Creating virtual environment..."
python3 -m venv "$APP_DIR/venv"
"$APP_DIR/venv/bin/pip" install --upgrade pip

echo "2. Installing Python dependencies..."
if [ -f "$REQUIREMENTS" ]; then
    "$APP_DIR/venv/bin/pip" install -r "$REQUIREMENTS"
else
    echo "?? No requirements.txt found at $REQUIREMENTS"
fi

# === CREATE SYSTEMD UNIT ===
echo "3. Creating systemd service..."

cat <<EOF | sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null
[Unit]
Description=Python Service: car-voice-control
After=network.target

[Service]
ExecStart=${PYTHON_BIN} ${MAIN_SCRIPT}
WorkingDirectory=${APP_DIR}
Restart=always
User=${USER_NAME}
Environment=PYTHONUNBUFFERED=1
StandardOutput=append:${LOG_FILE}
StandardError=append:${LOG_FILE}

[Install]
WantedBy=multi-user.target
EOF

# === ENABLE AND START SERVICE ===
echo "4. Reloading systemd and enabling service..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}.service
sudo systemctl restart ${SERVICE_NAME}.service

echo "? Service ${SERVICE_NAME} is now active."
echo "?? Logs: tail -f ${LOG_FILE}"
