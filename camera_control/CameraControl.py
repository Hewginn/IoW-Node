import picamera2

class Camera:

    # Initiate camera using PICAMERA libary
    def __init__(self):
        self.camera = picamera2.PiCamera2()
        self.camera.configure(picamera2.create_still_configuration())
    
    # Capture one image
    def takePicture(self, jpg_file: str):

        picamera2.start()
        picamera2.capture_file(jpg_file)
        picamera2.stop()
