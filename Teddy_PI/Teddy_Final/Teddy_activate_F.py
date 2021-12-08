import speak_F as tdsp
import record_F as tdrc
import RPi.GPIO as GPIO
from time import sleep
import random

# 사운드 센서 설정
GPIO.setmode(GPIO.BOARD)
soundpin = 7
GPIO.setup(soundpin, GPIO.IN)

# 녹화 시작 인사 추가
baby_name = '영희'
Hi = ['안녕', '반가워', '나랑 놀자', '나랑 얘기할래?']
speak_hi = f"{baby_name}, {random.sample(Hi, 2)}"

# 테디 동작
while True:
    soundlevel = GPIO.input(soundpin)
    print("soundlevel",soundlevel)

    if soundlevel >= 1 :
        tdsp.Speak_tts(speak_hi)
        tdrc.Camera_capture()
        tdrc.Record_voice()
        tdrc.Backend_uploading()
    
    else:
        tdsp.Speaktd()
        sleep(1)
