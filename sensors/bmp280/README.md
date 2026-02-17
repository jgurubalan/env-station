# BMP280 Sensor Module

Measures:
- Temperature (°C)
- Atmospheric Pressure (hPa)
- Calculated Altitude (m)

Interface: I2C

Output:
- data/logs/bmp280.csv
- data/latest/bmp280.json

Designed to operate independently so that:
- APRS module reads JSON
- Website reads CSV
- Future microcontroller can replace this module

