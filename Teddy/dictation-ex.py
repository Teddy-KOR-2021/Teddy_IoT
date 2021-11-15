import requests
import json

kakao_speech_url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
rest_api_key = '8e81dc17f5b57e2758df0f202ce099de'

headers = {
"Content-Type": "application/octet-stream",
"X-DSS-Service": "DICTATION",
"Authorization": "KakaoAK " + rest_api_key,
}
with open('output2.wav', 'rb') as fp:
    audio = fp.read()

res = requests.post(kakao_speech_url, headers=headers, data=audio)

print(res.text)
