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
#session = SessionControl.NodeSessionControl(SERVER_URL)


while(True):
    sensors[0].readData()
    temp = sensors[0].temperature
    hum = sensors[0].humidity

    print(f"The temperature is: {temp}, the humidity is: {hum}")

    time.sleep(10)

'''
    #Trying to connect to server
    if not session.isAuth:

        #Connecting to server and setting sensor and node values
        session.connect(PAGE_CONNECT, node.connect())
        if session.isAuth:
            node.setState(NODE_STATUS)
            node.server_control = session.updateNode(PAGE_NODE, node.details())
            for sensor in sensors:
                session.send(PAGE_SENSOR, sensor.details())
        else:
            node.setState(NodeControl.NodeState.Offline)
        
    else:
        #Setting node values and getting the server control
        node.server_control = session.updateNode(PAGE_NODE, node.details())

    if node.status == NodeControl.NodeState.Online and node.server_control:
        #Gathering sensor data
        datas = []
        for sensor in sensors:
            datas += sensor.getData()

        print(datas)

        #Sending HTTP post of sensors
        for data in datas:
            session.send(PAGE_DATA, data)

    time.sleep(DATA_SEND_FRQ)
'''