import sounddevice as sd
import soundfile as sf
import datetime
from picamera import PiCamera
from time import sleep
import os , sys
import boto3
import requests
import json
from pydub import AudioSegment, audio_segment
from pydub.playback import play
from io import BytesIO
from gtts import gTTS


s3 = boto3.client('s3')

# now = time.localtime()
nowtime = str(datetime.datetime.now().timestamp())[:10]
print(nowtime)
# 
# f"{now.tm_year}년{now.tm_mon}월{now.tm_mday}일{now.tm_hour}시{now.tm_min}분{now.tm_sec}초"



camera = PiCamera()
camera.resolution = (1024, 768)



fs = 44100
seconds = 7

# recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
# sd.wait()

# sf.write(f'{nowtime}.wav', recording, fs)

def startrun():
    
    mp3_redata = BytesIO()
    tts = gTTS('안녕! 반가워', lang='ko')
    tts.write_to_fp(mp3_redata)
    mp3_redata.seek(0)
    startspeak = AudioSegment.from_file(mp3_redata, format="mp3")
    play(startspeak)
    
    print("Start record")
    global now
    global nowtime
    camera.start_preview()
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    for i in range(3):
        sleep(1)
        camera.capture(f'/home/pi/Teddy_PI/image/{nowtime}0{i}.jpg')
    camera.stop_preview()
    sf.write(f'/home/pi/{nowtime}.wav', recording, fs)
    sleep(1)
    record_name = f'/home/pi/{nowtime}.wav'
    record_bucket ='kd1-teddy-records-bucket2021'
    record_key = f'records/{nowtime}.wav'
    s3.upload_file(record_name, record_bucket, record_key)
    # NEWCODE = f"aws s3 cp {nowtime}.wav s3://kd1-teddy-records-bucket2021/records/{nowtime}.wav"
    # os.system(NEWCODE)
    # for i in range(3):
    #     NEWCODE = f"aws s3 cp /home/pi/Teddy_PI/image/{nowtime}0{i}.jpg s3://kd1-teddy-records-bucket2021/image/{nowtime}0{i}.jpg"
    #     os.system(NEWCODE)  
    
    file_name = f'/home/pi/Teddy_PI/image/{nowtime}00.jpg'
    bucket =  'kd1-teddy-records-bucket2021'
    key = f'image/{nowtime}00.jpg'
    s3.upload_file(file_name, bucket, key)
    sleep(2)
    print("Upload start")
    headers = {'Content-Type': 'application/json; chearset=utf-8'}
    title = str(datetime.datetime.fromtimestamp(int(nowtime)))
    # titlename = datetime.datetime.fromtimestamp(int(timestamp))
    img_url = f"https://kd1-teddy-records-bucket2021.s3.eu-west-2.amazonaws.com/image/{nowtime}00.jpg"
    # img_url2 = f"https://kd1-teddy-records-bucket2021.s3.eu-west-2.amazonaws.com/image/{nowtime}01.jpg"
    # img_url3 = f"https://kd1-teddy-records-bucket2021.s3.eu-west-2.amazonaws.com/image/{nowtime}02.jpg"
    sound_url = f"https://kd1-teddy-records-bucket2021.s3.eu-west-2.amazonaws.com/records/{nowtime}.wav"
    data ={
            "imgUrl": img_url,
            # "imgUrl2": img_url2,
            # "imgUrl3": img_url3,
            "title":title,
            "soundUrl":sound_url}
    res = requests.post('http://18.169.185.73:8000/api/recordSound/create/',  data=json.dumps(data), headers=headers)
    print(str(res.status_code) + " | " + res.text)
    
    print("Upload OK")
    
    os.remove(f'/home/pi/{nowtime}.wav')
    print("Remove record file")
    sleep(1)
    for i in range(3):
        os.remove(f'/home/pi/Teddy_PI/image/{nowtime}0{i}.jpg')
    
    print("Complete")
        

startrun()