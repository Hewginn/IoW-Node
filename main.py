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
sensors = [
    SensorControl.DHT11(SENSORS["DHT11"]),
    SensorControl.GUVAS12SD(SENSORS["GUVAS12SD"])
]

# Initiating "Session"
session = SessionControl.NodeSessionControl(SERVER_URL)

# Initiating camera
camera = CameraControl.Camera()

# Cycle counter
number_of_cycles = 0

while(True):

    # Trying to connect to server
    if not session.isAuth:

        # Connecting to server and setting sensor and node values
        session.connect(PAGE_CONNECT, node.connect())
        if session.isAuth:
            node.setState(NODE_STATUS)
            node.server_control = session.updateNode(PAGE_NODE, node.details())
            for sensor in sensors:
                session.send(PAGE_SENSOR, sensor.details())
        else:
            node.setState(NodeControl.NodeState.Offline)
        
    else:
        # Setting node values and getting the server control
        node.server_control = session.updateNode(PAGE_NODE, node.details())

    if node.status == NodeControl.NodeState.Online and node.server_control:
        # Gathering sensor data
        datas = []
        for sensor in sensors:
            datas += sensor.getData()

        print(datas)

        # Sending HTTP post of sensors
        for data in datas:
            session.send(PAGE_DATA, data)

    # Sending image to server
    if number_of_cycles % 5 == 0:

        # Taking picture
        camera.takePicture(JPG_FILE)

        # Sending image
        session.sendImage(PAGE_IMAGE, JPG_FILE)
    
    # Incrementing number of cycles
    number_of_cycles += 1

    time.sleep(DATA_SEND_FRQ)