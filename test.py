
import board
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

i2c = board.I2C()

ads = ADS1115(i2c)

chan = AnalogIn(ads, ads1x15.Pin.A0)

print(chan.voltage)