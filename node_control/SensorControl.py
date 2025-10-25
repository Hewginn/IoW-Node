import adafruit_dht
import board
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

class Sensor():
    def __init__(self, sensor):
        self.is_online = sensor["is_online"]
        self.values = sensor["value_type"]
        self.name = 'DUMMY'
        
    def details(self):

        details = {
            'name': self.name,
            'status': 'Online' if self.is_online else 'Offline',
            'type': ', '.join(self.values),
        }

        return details

class DHT11(Sensor):

    def __init__(self, sensor):
        super().__init__(sensor)
        self.device = adafruit_dht.DHT11(board.D17)
        self.name = "DHT11"

    def readData(self):
        try:
            self.humidity = self.device.humidity
            self.temperature = self.device.temperature
        except RuntimeError:
            self.is_online = False


    def getData(self):
        self.readData()

        temperature_message = {
            "sensor_name": self.name,
            "value_type": "temperature",
            "value":  self.temperature,
            "unit": "C",
            "error_message": None,
        }

        humidity_message = {
            "sensor_name": self.name,
            "value_type": "humidity",
            "value":  self.humidity,
            "unit": "%",
            "error_message": None,
        }

        return [temperature_message, humidity_message]
    
class GUVAS12SD(Sensor):

    def __init__(self, sensor):
        super().__init__(sensor)
        self.name = "GUVAS12SD"

    def readData(self):
        # Create the I2C bus
        i2c = board.I2C()

        # Create the ADC object using the I2C bus
        ads = ADS1115(i2c)

        # Create single-ended input on channel 0
        chan = AnalogIn(ads, ads1x15.Pin.A0)

        mVoltage = ((chan.voltage / 65536) * 3.3) * 1000

        if mVoltage < 50:
            return 0
        elif mVoltage >= 227 and mVoltage < 318:
            return 1
        elif mVoltage >= 318 and mVoltage < 408:
            return 2
        elif mVoltage >= 408 and mVoltage < 503:
            return 3
        elif mVoltage >= 503 and mVoltage < 606:
            return 4
        elif mVoltage >= 606 and mVoltage < 696:
            return 5
        elif mVoltage >= 696 and mVoltage < 795:
            return 6
        elif mVoltage >= 795 and mVoltage < 881:
            return 7
        elif mVoltage >= 881 and mVoltage < 976:
            return 8
        elif mVoltage >= 976 and mVoltage < 1079:
            return 9
        elif mVoltage >= 1079 and mVoltage < 1170:
            return 10
        else: # anything greater than 1170
            return 11

    def getData(self):
        self.uv_index = self.readData()    

        uv_message = {
            "sensor_name": self.name,
            "value_type": "UV",
            "value":  self.uv_index,
            "unit": "UV inedx",
            "error_message": None,
        }

        return [uv_message]



        
