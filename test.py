import time
import pytest
from node_control.SensorControl import DHT11, GUVAS12SD
import config


class TestSensors:

    def test_DHT11_sensor(self):
        sensor: DHT11 = DHT11(config.SENSORS["DHT11"])

        sensor.readData()

        measured_temperatures = []
        measured_humidities = []

        for i in range(1,20):
            sensor.readData()
            measured_temperatures.append(sensor.temperature)
            measured_humidities.append(sensor.humidity)
            time.sleep(0.1)

        assert all(15 <= x <= 30 for x in measured_temperatures)
        assert len(set(measured_temperatures)) > 1
        assert all(30 <= x <= 70 for x in measured_humidities)
        assert len(set(measured_humidities)) > 1

    def test_UV_sensor(self):
        sensor: GUVAS12SD = GUVAS12SD(config.SENSORS["GUVAS12SD"])

        sensor.readData()

        measured_UVs = []

        for i in range(1,20):
            sensor.readData()
            measured_UVs.append(sensor.uv_intensity)
            time.sleep(0.1)

        assert all(0 <= x <= 10 for x in measured_UVs)
        assert len(set(measured_UVs)) > 1

