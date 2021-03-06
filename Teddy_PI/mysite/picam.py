import cv2
import io
from picamera.array import PiRGBArray
from picamera import PiCamera

class PiCam:
    def __init__(self, show=True, framerate=35, width=640, height=480, brightness=65):
        self.size = (width, height)
        self.show = show
        self.framerate = framerate
        self.brightness = brightness

        self.camera = PiCamera()
        self.camera.rotation = 180
        self.camera.resolution = self.size
        self.camera.framerate = self.framerate
        self.camera.brightness = self.brightness

    def __iter__(self): 
        rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
        rawCapture.truncate(0)
        for frame in self.camera.capture_continuous(rawCapture, format="bgr", 
                                                use_video_port=True):
            yield frame.array
            rawCapture.truncate(0)

    def run(self, callback=None):
        rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
        rawCapture.truncate(0)

        for frame in self.camera.capture_continuous(rawCapture, format="bgr",
                                                    use_video_port=True):
            image = frame.array
            if callback and not callback(image): break
            if(self.show or callback == None): 
                cv2.imshow('frame', image)
                key = cv2.waitKey(1)
                if key == 27: break
            rawCapture.truncate(0)

        cv2.destroyAllWindows()

class MJpegStreamCam(PiCam):
    def __init__(self, show=True, framerate=35, width=640, height=480, brightness=65):
        super().__init__(show=show, framerate=framerate, 
                        width=width, height=height, brightness=brightness)

    def __iter__(self): 
        frame = io.BytesIO()
        
        while True:
            self.camera.capture(frame, format="jpeg", use_video_port=True)
            image = frame.getvalue()
            yield (b'--myboundary\n'
                    b'Content-Type:image/jpeg\n'
                    b'Content-Length: ' + f"{len(image)}".encode() + b'\n'
                    b'\n' + image + b'\n')
            frame.seek(0)
            # time.sleep(1/self.framerate)
