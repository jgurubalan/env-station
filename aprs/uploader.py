import logging
import json
import time
from pathlib import Path
import signal
import sys
import aprslib

from config import CALLSIGN, PASSCODE, SERVER, PORT, UPLOAD_INTERVAL_SECONDS
from wx_formatter import format_wx_packet


BASE_PATH = Path(__file__).resolve().parent.parent
LATEST_FILE = BASE_PATH / "data" / "latest" / "bmp280.json"

running = True


# --------------------------
# Logging setup
# --------------------------
LOG_FILE = BASE_PATH / "logs" / "aprs_uploader.log"
LOG_FILE.parent.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# --------------------------
# Graceful shutdown handler
# --------------------------
def handle_exit(signum, frame):
    global running
    logging.info("Shutdown signal received. Stopping uploader.")
    running = False


signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)


print("APRS-IS Weather Uploader Started")
logging.info("APRS-IS Weather Uploader Started")


# --------------------------
# Main loop
# --------------------------
while running:
    try:
        logging.info("Connecting to APRS-IS...")

        ais = aprslib.IS(
            CALLSIGN,
            passwd=PASSCODE,
            host=SERVER,
            port=PORT
        )

        ais.connect()
        logging.info("Connected to APRS-IS")

        if LATEST_FILE.exists():
            with open(LATEST_FILE) as f:
                data = json.load(f)

            temperature = data["temperature_C"]
            pressure = data["pressure_hPa"]

            packet = format_wx_packet(CALLSIGN, temperature, pressure)

            ais.sendall(packet)
            logging.info(f"Packet sent successfully: {packet}")

        else:
            logging.warning("Sensor data file not found.")

        ais.close()
        logging.info("Connection closed cleanly.")

    except Exception as e:
        logging.error(f"Upload cycle failed: {e}")

    # Sleep with interrupt awareness
    for _ in range(UPLOAD_INTERVAL_SECONDS):
        if not running:
            break
        time.sleep(1)


logging.info("APRS uploader stopped.")
print("APRS uploader stopped.")
sys.exit(0)
