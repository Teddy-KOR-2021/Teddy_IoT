import requests
import json
import io
import soundfile as sf
import sounddevice as sd

kakao_speech_url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"

rest_api_key = '8e81dc17f5b57e2758df0f202ce099de'

headers = {
"Content-Type": "application/octet-stream",
"X-DSS-Service": "DICTATION",
"Authorization": "KakaoAK " + rest_api_key,
}

def recognize(audio):
    res = requests.post(kakao_speech_url,
            headers=headers, data=audio)
    
    try:
        result_json_string = res.text[
            res.text.index('{type":"finalResult"'):res.text.rindex('}')+1
        ]
        result = json.loads(result_json_string)
        value = result['value']
    except: # 인식 실패
        value = None
    
    return value

def record(duration=5, fs=16000, channels=1):
    data = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    audio = io.BytesIO()
    sf.write(audio, data, fs, format="wav")
    audio.seek(0)

    return audio

if __name__ == '__main__':
    audio = record()
    value = recognize(audio)
    print('[인식결과]', value)