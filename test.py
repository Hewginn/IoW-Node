import time
import pytest
from node_control.SensorControl import DHT11, GUVAS12SD
from camera_control.CameraControl import RaspberryPiCameraModuleV2
import config
import numpy as np
from PIL import Image
import shutil


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

class TestCamera:
    def test_camera(self):
        camera: RaspberryPiCameraModuleV2 = RaspberryPiCameraModuleV2(config.CAMERAS["RaspberryPi Camera Module V2"])

        shutil.copy("/camera_control/images/test.jpg", camera.path)

        time.sleep(1)

        before_image = np.array(Image.open(camera.path))

        time.sleep(1)

        after_image = np.array(Image.open(camera.path))

        assert not np.array_equal(before_image, after_image)