import record as tdrc
import speak as tdsp
import RPi.GPIO as GPIO
from time import sleep
import paho.mqtt.client as mqtt

mqtt_client = mqtt.Client()
mqtt_client.on_connect = tdsp.on_connect
mqtt_client.on_message = tdsp.on_message


GPIO.setmode(GPIO.BOARD)
soundpin = 7
GPIO.setup(soundpin, GPIO.IN)

while 1:
    soundlevel = GPIO.input(soundpin)
    if soundlevel == 1 :
        
        tdrc.run()
    else:
        tdsp.speaktd()
    

