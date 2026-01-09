from picamera2 import Picamera2
import time

class Camera:

    # Initiate camera using PICAMERA libary
    def __init__(self):
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_still_configuration())
    
    # Capture one image
    def takePicture(self, jpg_file: str):

        self.camera.start()
        time.sleep(1)
        self.camera.capture_file(jpg_file)
        self.camera.stop()
