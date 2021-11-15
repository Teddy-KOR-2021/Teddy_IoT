from gtts import gTTS

import os

tts = gTTS(text= '안녕, 나는 공감이야!', lang = 'ko')

tts.save("example.mp3")

