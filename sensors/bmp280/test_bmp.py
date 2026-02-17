import board
import busio
import adafruit_bmp280

i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

print("Temperature:", round(bmp280.temperature, 2), "C")
print("Pressure:", round(bmp280.pressure, 2), "hPa")
