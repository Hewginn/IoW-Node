import adafruit_dht
from board import D17

class Sensor():
    def __init__(self, sensor):
        self.is_online = sensor["is_online"]
        self.values = sensor["value_type"]
        self.name = 'DUMMY'

    def createOfflineMessage(self):
        #Setting sensor status on server side in post
        pass
        
    def turnOffline(self):
        #In case of error use this
        self.is_online = False

    def turnOnline(self):
        #Turn on sensor
        self.is_online = True

    def getData(self):
        pass
        
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
        self.device = adafruit_dht.DHT11(D17)
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
        self.uv = 30

    def getData(self):
        self.readData()    

        uv_message = {
            "sensor_name": self.name,
            "value_type": "UV",
            "value":  self.uv,
            "unit": "UV",
            "error_message": None,
        }

        return [uv_message]



        
