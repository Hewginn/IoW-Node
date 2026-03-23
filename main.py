from config import *
from node_control import SensorControl, NodeControl
from communication_control import SessionControl
from camera_control import CameraControl
import time

class MainController:
    def __init__(self):

        #Initiating Node
        self.node = NodeControl.Node(
            NODE_NAME,
            NODE_PASSWORD,
            NODE_STATUS,
            NODE_LOCATION,
            NODE_MAIN_UNIT
        )

        # Initiating Sensors
        self.sensors: list[SensorControl.Sensor] = [
            SensorControl.DHT11(SENSORS["DHT11"]),
            SensorControl.GUVAS12SD(SENSORS["GUVAS12SD"])
        ]

        # Initiating "Session"
        self.session = SessionControl.NodeSessionControl(SERVER_URL)

        # Initiating camera
        self.cameras: list[CameraControl.Camera] = [
            CameraControl.RaspberryPiCameraModuleV2(CAMERAS["RaspberryPi Camera Module V2"])
        ]

        self.is_node_faulty = False

        self.counter = 0


    def connecting(self):
        # Trying to connect to server
        if not self.session.isAuth:

            # Connecting to server and setting sensor and node values
            try:
                self.session.connect(PAGE_CONNECT, self.node.connect())
                if self.session.isAuth:
                    self.node.setState(NODE_STATUS)
                    self.node.server_control = self.session.updateNode(PAGE_NODE, self.node.details())
                    for sensor in self.sensors:
                        self.session.send(PAGE_SENSOR, sensor.details())
                    for camera in self.cameras:
                        self.session.send(PAGE_CAMERA, camera.details())
            except Exception as e:
                print(f"Exception error: {e}")
                self.node.setState(NodeControl.NodeState.Offline)
        else:
            # Setting node values and getting the server control
            self.node.server_control = self.session.updateNode(PAGE_NODE, self.node.details())

    def measurement(self):
        # Gathering sensor data
        data = []
        for sensor in self.sensors:
            # Getting the sensor data and adding to other data
            sensor_data = sensor.getData()
            data += sensor_data
            # Sending sensor info if the status changed
            if sensor.changed_state:
                self.session.send(PAGE_SENSOR, sensor.details())
                sensor.changed_state = False
            self.is_node_faulty = self.is_node_faulty or not sensor.is_online
        print(data)
        # Sending HTTP post of sensors
        for item in data:
            self.session.send(PAGE_DATA, item)

    def camera(self):

        for camera in self.cameras:

            # Getting and sending the image
            image_message = camera.getImageMessage()
            self.session.sendImage(PAGE_IMAGE, camera.path, image_message)

            # Sending camera info if the status changed
            if camera.changed_state:
                self.session.send(PAGE_CAMERA, camera.details())
                camera.changed_state = False

    def changeState(self):
        # Setting faulty state if one sensor or camera is offline
        if self.is_node_faulty:
            self.node.setState(NodeControl.NodeState.Faulty)
        else:
            self.node.setState(NODE_STATUS)

    def run(self):

        self.is_node_faulty = False
        self.connecting()

        # Sending data if the Node is not offline and the server approves
        if self.node.status != NodeControl.NodeState.Offline and self.node.server_control:
            self.measurement()
            if self.counter % IMG_SEND_COUNTER == 0:
                self.camera()
            for camera in self.cameras:
                self.is_node_faulty = self.is_node_faulty or not camera.is_online
            self.changeState()
        
        self.counter = self.counter + 1

def main():
    main_controller = MainController()
    while(True):
        try:
            main_controller.run()
        except Exception as e:
            print(f"Runtime error: {e}")
        time.sleep(DATA_SEND_FRQ)

if __name__ == "__main__":
    main()

