import speak_F as tdsp
import record_F as tdrc
from time import sleep
import random
import spidev, time


# 사운드 센서 설정
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 100000

def analog_read(channel):
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_data = ((r[1]&3) << 8) + r[2]

    return adc_data

# 녹화 시작 인사 추가
baby_name = '영희'
Hi = ['안녕', '만나서 반가워!', '나랑 놀자!', '나랑 얘기할래?', '하하']

# mqtt 브로커 연동
tdsp.Speaktd()

# 테디 동작
while True:

    soundlevel = analog_read(0)
    speak_hi = f"{baby_name}, {random.sample(Hi, 2)}"

    if soundlevel >= 200 :
        tdsp.Speak_tts(speak_hi)
        tdrc.Camera_capture()
        tdrc.Record_voice()
        tdrc.Backend_uploading()
    
    else:
        tdsp.Speaktd()
        sleep(1)
