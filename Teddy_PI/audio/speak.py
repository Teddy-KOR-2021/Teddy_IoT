from gtts import gTTS
import gtts
import playsound
import paho.mqtt.client as mqtt
import os
from time import sleep
import random
from io import BytesIO
from pydub import AudioSegment, audio_segment
from pydub.playback import play

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK")
        client.subscribe("iot")
    else:
        print('실패')

def on_message(client, userdata, msg):
    speak_text = str(msg.payload.decode("utf-8"))
    print(speak_text)
    mp3_data = BytesIO()
    tts = gTTS(f'{speak_text}', lang='ko')
    tts.write_to_fp(mp3_data)
    mp3_data.seek(0)
    song = AudioSegment.from_file(mp3_data, format="mp3")
    play(song)


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

try :
    mqtt_client.connect('18.169.185.73', 1883)
    mqtt_client.loop_start()

except Exception as err:
    print('에러 : %s'%err)