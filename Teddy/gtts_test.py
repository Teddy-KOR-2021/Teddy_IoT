from gtts import gTTS

import os

tts = gTTS(text= 'good morning', lang = 'en')

tts.save("good.mp3")

