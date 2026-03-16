from config import *
from node_control import SensorControl, NodeControl
from communication_control import SessionControl
from camera_control import CameraControl
import time

# Initiating Node
node = NodeControl.Node(
    NODE_NAME,
    NODE_PASSWORD,
    NODE_STATUS,
    NODE_LOCATION,
    NODE_MAIN_UNIT
)

# Initiating Sensors
sensors: list[SensorControl.Sensor] = [
    SensorControl.DHT11(SENSORS["DHT11"]),
    SensorControl.GUVAS12SD(SENSORS["GUVAS12SD"])
]

# Initiating "Session"
session = SessionControl.NodeSessionControl(SERVER_URL)

# Initiating camera
cameras: list[CameraControl.Camera] = [
    CameraControl.RaspberryPiCameraModuleV2(CAMERAS["RaspberryPi Camera Module V2"])
]

# Cycle counter
number_of_cycles = 0

while(True):

    # Trying to connect to server
    if not session.isAuth:

        # Connecting to server and setting sensor and node values
        try:
            session.connect(PAGE_CONNECT, node.connect())
            if session.isAuth:
                node.setState(NODE_STATUS)
                node.server_control = session.updateNode(PAGE_NODE, node.details())
                for sensor in sensors:
                    session.send(PAGE_SENSOR, sensor.details())
                for camera in cameras:
                    session.send(PAGE_CAMERA, camera.details())
        except Exception as e:
            node.setState(NodeControl.NodeState.Offline)
    else:
        # Setting node values and getting the server control
        node.server_control = session.updateNode(PAGE_NODE, node.details())

    # Sending data if the Node is not offline and the server approves
    if node.status != NodeControl.NodeState.Offline and node.server_control:

        is_node_faulty = False

        # Gathering sensor data
        data = []
        for sensor in sensors:

            # Getting the sensor data and adding to other data
            sensor_data = sensor.getData()
            data += sensor_data

            # Sending camera info if the status changed
            if sensor.changed_state:
                session.send(PAGE_SENSOR, sensor.details())
                sensor.changed_state = False
            is_node_faulty = is_node_faulty or not sensor.is_online

        print(data)

        # Sending HTTP post of sensors
        for data in data:
            session.send(PAGE_DATA, data)

        # Sending image to server
        if number_of_cycles % 5 == 0:

            for camera in cameras:

                # Getting and sending the image
                image_message = camera.getImageMessage()
                session.sendImage(PAGE_IMAGE, camera.path, image_message)

                # Sending camera info if the status changed
                if camera.changed_state:
                    session.send(PAGE_CAMERA, camera.details())
                    camera.changed_state = False

                # The node is faulty if one camera is faulty
                is_node_faulty = is_node_faulty or not camera.is_online

        # Setting faulty state if one sensor or camera is offline
        if is_node_faulty:
            node.setState(NodeControl.NodeState.Faulty)
    
    # Incrementing number of cycles
    number_of_cycles += 1

    time.sleep(DATA_SEND_FRQ)