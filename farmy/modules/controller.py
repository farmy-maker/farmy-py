# coding: utf-8
import RPi.GPIO as GPIO
import time


class Controller:

    def __init__(self, pin):
        self.pin = pin

    def run(self, power, seconds):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)
        obj = GPIO.PWM(self.pin, 100)
        obj.start(0)
        obj.ChangeDutyCycle(power)
        time.sleep(seconds)
        obj.stop()
        GPIO.cleanup()

    def turn_on(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def flash(self):
        self.run(100, 3)

    def flash_long(self):
        self.run(100, 10)
