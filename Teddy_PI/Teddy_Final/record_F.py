import sounddevice as sd
import soundfile as sf
import datetime
from picamera import PiCamera
from time import sleep
import os
import boto3
import requests
import json

s3 = boto3.client('s3')
nowtime = str(datetime.datetime.now().timestamp())[:10]

def Camera_capture(): # 아이 이미지 캡쳐, s3 버킷에 이미지파일 업로드
    camera = PiCamera()
    camera.resolution = (1024, 768)

    print("Start capture")
    camera.start_preview()
    sleep(1)
    camera.capture(f'/home/pi/Teddy_PI/image/{nowtime}00.jpg')
    camera.stop_preview()
    sleep(1)

    image_name = f'/home/pi/Teddy_PI/image/{nowtime}00.jpg'
    image_bucket =  'kd1-teddy-records-bucket2021'
    key = f'image/{nowtime}00.jpg'
    s3.upload_file(image_name, image_bucket, key)
    print("Upload OK")

def Record_voice(): #아이 목소리 녹음, s3 버킷에 음성파일 업로드
    fs = 44100
    seconds = 7

    print("Start record")
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    sf.write(f'/home/pi/{nowtime}.wav', recording, fs)
    sleep(1)

    record_name = f'/home/pi/{nowtime}.wav'
    record_bucket ='kd1-teddy-records-bucket2021'
    record_key = f'records/{nowtime}.wav'
    s3.upload_file(record_name, record_bucket, record_key)
    print("Upload OK")

def Backend_uploading(): #장고에 음성파일과 이미지파일 POST

    print("POST start")
    headers = {'Content-Type': 'application/json; chearset=utf-8'}
    title = str(datetime.datetime.fromtimestamp(int(nowtime)))
    img_url = f"https://kd1-teddy-records-bucket2021.s3.eu-west-2.amazonaws.com/image/{nowtime}00.jpg"
    sound_url = f"https://kd1-teddy-records-bucket2021.s3.eu-west-2.amazonaws.com/records/{nowtime}.wav"
    data ={
            "imgUrl": img_url,
            "title":title,
            "soundUrl":sound_url
    }
    
    res = requests.post('http://18.169.185.73:8000/api/recordSound/create/',  data=json.dumps(data), headers=headers)
    print(str(res.status_code) + " | " + res.text)
    print("POST OK")
    # POST 후 라즈베리파이 내 저장 파일 제거
    os.remove(f'/home/pi/{nowtime}.wav')
    os.remove(f'/home/pi/Teddy_PI/image/{nowtime}00.jpg')
    print("Complete")









