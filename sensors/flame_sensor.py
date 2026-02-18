import RPi.GPIO as GPIO
import time
# 4591 module
# Pin setup
FLAME_PIN = 17  # you can change this to any GPIO pin

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLAME_PIN, GPIO.IN)

try:
    print("Flame sensor test (CTRL+C to exit)")
    while True:
        sensor_state = GPIO.input(FLAME_PIN)

        if sensor_state == GPIO.LOW:
            print("🔥 Flame detected!")
        else:
            print("✅ No flame detected")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nExiting…")

finally:
    GPIO.cleanup()
