from gtts import gTTS
import gtts
import playsound
import paho.mqtt.client as mqtt
import os
from time import sleep

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"연결 결과 {rc}")
    if rc == 0:
        client.subscribe("$SYS/#")
    else:
        print('연결 실패 :  ', rc)

def on_message(client, userdata, msg):
    speakted = str(msg.payload.decode())
    tts = gTTS(text=speakted, lang='ko')
    filename = 'textmessage.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    sleep(10)
    os.remove('textmessage.mp3')
    print(f"{speakted}")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

try :
    mqtt_client.connect("localhost")
    mqtt_client.loop_forever()

except Exception as err:
    print('에러 : %s'%err)