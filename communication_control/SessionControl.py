import requests
import json

class NodeSessionControl():
    def __init__(self, server):
        self.server = server
        self.isAuth = False
        self.serverResponding = True
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    #Adding new token to the session
    def addToken(self, token):
        self.headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    #Delete Token
    def deleteToken(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
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

        # Print response
        print(response.status_code)
        print(response.text)

        #Checking if connected succesfully
        if response.status_code == 401:
            self.isAuth = False


    def updateNode(self, page, payload):
        if not self.isAuth:
            return False

        #Sending HTTP post
        response = requests.post(self.server + page, json=payload, headers=self.headers)

        # Print response
        print(response.status_code)
        print(response.text)


        #Checking if connected succesfully
        if response.status_code == 401:
            self.isAuth = False
            return False
        elif response.status_code != 200:
            return False

        if 'control' in response.json():
            return response.json()['control']
        
    def sendImage(self, page, jpg_file: str):

        with open(jpg_file, "rb") as img:
            files = {"image": ("photo.png", img, "image/png")}
            response = requests.post(self.server + page, files=files)

        print(response.json())


    

