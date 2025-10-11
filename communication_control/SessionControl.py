import requests
import json

class NodeSessionControl():
    def __init__(self, server):
        self.server = server
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

        self.addToken(response.json()['token'])

    #Sending HTTP posts
    def send(self, page, payload):

        #Sending HTTP post
        response = requests.post(self.server + page, json=payload, headers=self.headers)

        # Print response
        print(response.status_code)
        print(response.text)

    

