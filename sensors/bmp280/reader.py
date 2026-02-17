import time
import csv
import json
import signal
import sys
from datetime import datetime, timezone
from pathlib import Path

import board
import busio
import adafruit_bmp280


# =========================
# CONFIGURATION
# =========================

I2C_ADDRESS = 0x76
READ_INTERVAL_SECONDS = 60
SEA_LEVEL_PRESSURE_HPA = 1013.25


# =========================
# PATH SETUP
# =========================

BASE_PATH = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_PATH / "data"
LOG_DIR = DATA_DIR / "logs"
LATEST_DIR = DATA_DIR / "latest"

LOG_FILE = LOG_DIR / "bmp280.csv"
LATEST_FILE = LATEST_DIR / "bmp280.json"

LOG_DIR.mkdir(parents=True, exist_ok=True)
LATEST_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# GRACEFUL SHUTDOWN
# =========================

running = True

def handle_exit(signum, frame):
    global running
    print("\nStopping BMP280 logger cleanly...")
    running = False

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)


# =========================
# SENSOR INITIALIZATION
# =========================

i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=I2C_ADDRESS)
bmp280.sea_level_pressure = SEA_LEVEL_PRESSURE_HPA


# =========================
# INITIALIZE CSV HEADER
# =========================

if not LOG_FILE.exists():
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp_utc",
            "temperature_C",
            "pressure_hPa",
            "altitude_m"
        ])


# =========================
# MAIN LOOP
# =========================

print("BMP280 Logger Started")
print(f"Logging to: {LOG_FILE}")
print(f"Latest JSON: {LATEST_FILE}")
print("-" * 50)

while running:
    try:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        temperature = round(bmp280.temperature, 2)
        pressure = round(bmp280.pressure, 2)
        altitude = round(bmp280.altitude, 2)

        # Append to CSV
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                temperature,
                pressure,
                altitude
            ])

        # Update latest JSON
        latest_data = {
            "timestamp_utc": timestamp,
            "temperature_C": temperature,
            "pressure_hPa": pressure,
            "altitude_m": altitude
        }

        with open(LATEST_FILE, "w") as f:
            json.dump(latest_data, f, indent=4)

        print(latest_data)

    except Exception as e:
        print("Error reading BMP280:", e)

    # Interruptible sleep (immediate Ctrl+C exit)
    for _ in range(READ_INTERVAL_SECONDS):
        if not running:
            break
        time.sleep(1)

print("BMP280 Logger Stopped.")
sys.exit(0)
