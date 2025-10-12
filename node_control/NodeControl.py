from enum import Enum

class NodeState(Enum):
    Offline = 0
    Online = 1
    Development = 2
    Faulty = 3

    String = [
        'Offline',
        'Online',
        'In Development',
        'Faulty',
    ]

class Node():

    def __init__(self, name: str, password: str, status: NodeState, location: str, main_unit: str):
        self.name = name
        self.password = password
        self.status = status
        self.location = location
        self.main_unit = main_unit
        self.server_control = False
    
    #Creating log in message
    def connect(self):
        credentials = {
            'name': 'NODE_1',
            'password': 'node1234',
        }
        return credentials
    
    #Setting state
    def setState(self, state: NodeState):
        self.status = state
    
    #Creating node details message
    def details(self):
        
        details = {
            'location': self.location,
            'status': NodeState.String[self.status.value],
            'main_unit': self.main_unit,
        }

        return details
