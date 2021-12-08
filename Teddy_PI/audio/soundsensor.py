import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
soundpin = 7
GPIO.setup(soundpin, GPIO.IN)

while 1:
    soundlevel = GPIO.input(soundpin)
    print("soundlevel",soundlevel)
    sleep(1)

