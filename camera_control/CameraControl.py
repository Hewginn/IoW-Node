from picamera2 import Picamera2

class Camera:

    # Initiate camera using PICAMERA libary
    def __init__(self):
        self.camera = Picamera2()
        self.capture_config = self.camera.create_still_configuration()
    
    # Capture one image
    def takePicture(self, jpg_file: str):

        self.camera.start()
        self.camera.switch_mode_and_capture_file(self.capture_config, jpg_file)
        self.camera.stop()
