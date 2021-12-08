from gtts import gTTS
import paho.mqtt.client as mqtt
from io import BytesIO
from pydub import AudioSegment, audio_segment
from pydub.playback import play


def on_connect(client, userdata, flags, rc): # iot topic 으로 메세지 발행
    if rc == 0:
        print("Connected OK")
        client.subscribe("iot")
    else:
        print('실패')

def on_message(client, userdata, msg): # 메세지 데이터 수신 on_message, 데이터 tts로 전달
    message_text = str(msg.payload.decode("utf-8"))
    print(message_text)

    return Speak_tts(message_text)
    
def Speak_tts(text): # 메세지 데이터 gtts 모듈로 바로 실행 text = message
    speak_text = text
    mp3_data = BytesIO()
    tts = gTTS(f'{speak_text}', lang='ko')
    tts.write_to_fp(mp3_data)
    mp3_data.seek(0)
    speakdata = AudioSegment.from_file(mp3_data, format="mp3")
    play(speakdata)

def Speaktd(): # 새로운 클라이언트 생성 mqtt_client, 콜백 함수 설정 on_connect(브로커에 접속)
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    try :
        mqtt_client.connect('18.169.185.73', 1883)
        mqtt_client.loop_start()

    except Exception as err:
        print('에러 : %s'%err)

Speaktd()