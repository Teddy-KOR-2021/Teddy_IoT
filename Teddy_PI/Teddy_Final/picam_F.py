from picamera import PiCamera
from time import sleep

class PiCam: 

    # 라즈베리 파이 카메라 속성 설정 fps, 크기, 밝기, 조감도
    def __init__(self, show=True, framerate=35, width=1024, height=768, brightness=55, iso=100):
        self.size = (width, height)
        self.show = show
        self.framerate = framerate
        self.brightness = brightness
        self.iso = iso

        self.camera = PiCamera()
        self.camera.rotation = 180
        self.camera.resolution = self.size
        self.camera.framerate = self.framerate
        self.camera.brightness = self.brightness
        self.camera.iso = self.iso
    
    # 카메라 촬영
    def image_capture(self, image_adress):
        

        self.camera.start_preview()
        sleep(1)
        self.camera.capture(f'{image_adress}.jpg')
        self.camera.stop_preview()
