import sounddevice as sd
import soundfile as sf
import time
from picamera import PiCamera
from time import sleep
import os , sys

now = time.localtime()
nowtime = f"{now.tm_year}년{now.tm_mon}월{now.tm_mday}일{now.tm_hour}시{now.tm_min}분{now.tm_sec}초"

camera = PiCamera()
camera.resolution = (1024, 768)



fs = 44100
seconds = 15

# recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
# sd.wait()

# sf.write(f'{nowtime}.wav', recording, fs)

def run():
    global now
    global nowtime
    camera.start_preview()
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    for i in range(3):
        sleep(3)
        camera.capture(f'/home/pi/Teddy_PI/image/{nowtime}-{i}.jpg')
    camera.stop_preview()
    sf.write(f'/home/pi/{nowtime}.wav', recording, fs)
    sleep(2)
    NEWCODE = f"aws s3 cp {nowtime}.wav s3://kd1-teddy-records-bucket2021/records/{nowtime}.wav"
    os.system(NEWCODE)
run()