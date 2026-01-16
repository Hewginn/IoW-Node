from picamera2 import Picamera2
import time

class Camera:

    # Initiate camera
    def __init__(self, camera):
        self.name = "DUMMY"
        self.resolution = camera["resolution"]
        self.is_online = camera["is_online"]
        self.path = camera["used_jpg_file"]

    def details(self):
        details = {
            'name': self.name,
            'resolution': self.resolution[0] + "x" + self.resolution[1],
            'status': 'Online' if self.is_online else 'Offline',
        }

        return details
    
    # Capture one image
    def takePicture(self):
        return self.path
    
class RaspberryPiCameraModuleV2(Camera):
    # Initiate camera using PICAMERA libary
    def __init__(self, camera):
        super().__init__(camera)
        self.name = "RaspberryPi Camera Module V2"
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_still_configuration(
            main={"size": self.resolution}
        ))
    
    # Capture one image
    def takePicture(self):
        try:
            self.camera.start()
            time.sleep(1)
            self.camera.capture_file(self.path)
            self.camera.stop()
        except Exception as e:
            return "ERROR: Couldn't take picture!"
        
        return None


    def getImageMessage(self):
        
            error_message = self.takePicture()

            payload = {
                "camera_name": self.name,
                "error_message": error_message,
            }

            return payload