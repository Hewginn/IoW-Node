from node_control import SensorControl
import config
import time

guva = SensorControl.GUVAS12SD(config.SENSORS["GUVAS12SD"])
dht = SensorControl.DHT11(config.SENSORS["DHT11"])

while(True):

    print(f"Temperature and humidity:\n{dht.getData()}")

    print(f"UV voltage:\n{guva.getData()}")

    time.sleep(10)