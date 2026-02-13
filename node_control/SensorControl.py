import adafruit_dht
import board
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

# Abstract class for sensors
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

# DHT11 temperature and humidity sensor
class DHT11(Sensor):

    def __init__(self, sensor):
        super().__init__(sensor)
        self.device = adafruit_dht.DHT11(board.D17)
        self.name = "DHT11"

    # Read temperature and humidity
    def readData(self):
        try:
            self.humidity = self.device.humidity
            self.temperature = self.device.temperature
        except RuntimeError as e:
            print(str(e))
            self.is_online = False
            self.humidity = 0
            self.temperature = 0
            return "ERROR: Couldn't make measurement!"

        return None

    # Create payload message for server
    def getData(self):
        error_message = self.readData()

        temperature_message = {
            "sensor_name": self.name,
            "value_type": "temperature",
            "value":  self.temperature,
            "unit": "C",
            "error_message": error_message,
        }

        humidity_message = {
            "sensor_name": self.name,
            "value_type": "humidity",
            "value":  self.humidity,
            "unit": "%",
            "error_message": error_message,
        }

        return [temperature_message, humidity_message]
    
class GUVAS12SD(Sensor):

    def __init__(self, sensor):
        super().__init__(sensor)

        self.name = "GUVAS12SD"

        # Create the I2C bus
        self.i2c = board.I2C()

        # Create the ADC object using the I2C bus
        self.ads = ADS1115(self.i2c)

        # Create single-ended input on channel 0
        self.chan = AnalogIn(self.ads, ads1x15.Pin.A0)


    # Read UV values
    def readData(self):
        try:
            # Calibration of measured voltage
            self.uv_intensity = self.chan.voltage * 2.09 # mW/cm2

        except Exception as e:
            print(str(e))
            self.uv_intensity = 0
            return "ERROR: Couldn't make measurement!"
        
        return None

    #Creating payload messsage for server
    def getData(self):
        error_message = self.readData()    

        uv_message = {
            "sensor_name": self.name,
            "value_type": "UV",
            "value":  self.uv_intensity,
            "unit": "mW/cm2",
            "error_message": error_message,
        }

        return [uv_message]



        
