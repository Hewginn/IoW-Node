#This file contains the device specific configurations. Should be modified when adding a new device.

#Addresses for the server
SERVER_URL = 'http://192.168.0.157:29083'

PAGE_CONNECT = '/api/nodeLogin'
PAGE_NODE = '/api/updateNode'
PAGE_SENSOR = '/api/updateSensors'
PAGE_DATA = '/api/sendData'

#ID of the node
NODE_NAME = 'NODE_1'
NODE_PASSWORD = 'node1234'
NODE_STATUS = 1
NODE_NAME = "Main Unit"
NODE_LOCATION = "Felsoors Szegedi Roza utca 9."
NODE_MAIN_UNIT = "Raspberry Pi 4 Model B"


#The implemented sensors
#In case of implementing a new sensors the following files should be updated:
#   sensor_data_control.py
SENSORS = {
    "DHT11":{
        "is_online": True,
        "value_type": [
            "humidity",
            "temperature",
        ]
    },
    "GUVAS12SD":{
        "is_online": False,
        "value_type": [
            "UV",
        ],
    },
}

#The frequency of sending HTTP posts
DATA_SEND_FRQ = 60 
