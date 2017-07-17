# coding: utf-8
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
PIN_PUMP = 24
GPIO.setup(PIN_PUMP, GPIO.OUT, initial=GPIO.LOW)


def run_pwm(pin, power, seconds):
    obj = GPIO.PWM(pin, 100)
    obj.start(0)
    obj.ChangeDutyCycle(power)
    time.sleep(seconds)
    obj.stop()
