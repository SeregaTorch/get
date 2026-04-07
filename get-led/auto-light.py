import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led = 16
GPIO.setup(led, GPIO.OUT)
chel = 6
GPIO.setup(chel, GPIO.IN)
state = 0
while True:
    sensor_value = GPIO.input(chel)
    GPIO.output(led, not sensor_value)
    