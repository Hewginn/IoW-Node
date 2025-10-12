import requests
import json

class NodeSessionControl():
    def __init__(self, server):
        self.server = server
        self.isAuth = False
        self.serverResponding = True
        self.headers = {
            'Content-Type': 'application/json',
        }

    #Adding new token to the session
    def addToken(self, token):
        self.headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
        }

    #Delete Token
    def deleteToken(self):
        self.headers = {
            'Content-Type': 'application/json',
        }

    #Sending credentials and saving the token
    def connect(self, page, payload):
        #Sending HTTP post
        response = requests.post(self.server + page, json=payload, headers=self.headers)

        # Print response
        print(response.status_code)
        print(response.text)

        if response.status_code == 200:
            self.isAuth = True
            self.addToken(response.json()['token'])
        else:
            self.isAuth = False
            self.deleteToken()

    #Sending HTTP posts
    def send(self, page, payload):
        if not self.isAuth:
            return

        #Sending HTTP post
        response = requests.post(self.server + page, json=payload, headers=self.headers)

        #Checking if connected succesfully
        if response.status_code == 401:
            self.isAuth = False

        # Print response
        print(response.status_code)
        print(response.text)


    def updateNode(self, page, payload):
        if not self.isAuth:
            return False

        #Sending HTTP post
        response = requests.post(self.server + page, json=payload, headers=self.headers)

        #Checking if connected succesfully
        if response.status_code == 401:
            self.isAuth = False
            return False
        elif response.status_code != 200:
            return False

        # Print response
        print(response.status_code)
        print(response.text)

        if 'control' in response.json():
            return response.json()['control']

    

