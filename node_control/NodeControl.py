class Node():

    def __init__(self, name, password, status, location, main_unit):
        self.name = name
        self.password = password
        self.status = status
        self.location = location
        self.main_unit = main_unit
    
    #Creating log in message
    def connect(self):
        credentials = {
            'name': 'NODE_1',
            'password': 'node1234',
        }
        return credentials
    
    #Creating node details message
    def details(self):
        if self.status == 0:
            status_str = 'Offline'
        elif self.status == 1:
            status_str = 'Online'
        elif self.status == 2:
            status_str = 'In Development'
        elif self.status == 3:
            status_str = 'Faulty'
        else:
            status_str = 'Unknown'

        details = {
            'location': self.location,
            'status': status_str,
            'main_unit': self.main_unit,
        }

        return details
