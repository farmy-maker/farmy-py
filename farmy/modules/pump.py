# coding: utf-8
import RPi.GPIO as GPIO
import time

PIN_PUMP = 24


def run_pwm(pin, power, seconds):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
    obj = GPIO.PWM(pin, 100)
    obj.start(0)
    obj.ChangeDutyCycle(power)
    time.sleep(seconds)
    obj.stop()
    GPIO.cleanup()
