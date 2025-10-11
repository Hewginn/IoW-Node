from config import *
from node_control import SensorControl, NodeControl
from communication_control import SessionControl
import time

#Initiating Node
node = NodeControl.Node(
    NODE_NAME,
    NODE_PASSWORD,
    NODE_STATUS,
    NODE_LOCATION,
    NODE_MAIN_UNIT
)

#Initiating Sensors
sensors = [
    SensorControl.DHT11(SENSORS["DHT11"]),
    SensorControl.GUVAS12SD(SENSORS["GUVAS12SD"])
]

#Initiating "Session"
session = SessionControl.NodeSessionControl(SERVER_URL)

#Get token
session.connect(PAGE_CONNECT, node.connect())

#Update node and sensors on server
session.send(PAGE_NODE, node.details())
for sensor in sensors:
    session.send(PAGE_SENSOR, sensor.details())


while(True):

    #Gathering sensor data
    datas = []
    for sensor in sensors:
        datas += sensor.getData()

    print(datas)

    #Sending HTTP post of sensors
    for data in datas:
        session.send(PAGE_DATA, data)

    time.sleep(DATA_SEND_FRQ)
