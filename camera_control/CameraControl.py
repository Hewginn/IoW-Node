import picamera

class Camera:

    # Initiate camera using PICAMERA libary
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1280,720)
    
    # Capture one image
    def takePicture(self, jpg_file: str):

        # Opening used jpg file on client
        my_file = open(jpg_file, 'wb')

        #Capturing image
        self.camera.capture(jpg_file)

        #Closing file
        my_file.close()