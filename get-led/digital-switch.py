import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led = 23
GPIO.setup(led, GPIO.OUT)
button = 13
GPIO.setup(button, GPIO.IN)
state = 0
status = 0
while True:
    if GPIO.input(button) and status == 0 :
        state = not state
        GPIO.output(led, state)
        time.sleep(0.2)
        status = 1
    elif status == 1 and (not GPIO.input(button)) :
        status = 0