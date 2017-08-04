# coding: utf-8
import RPi.GPIO as GPIO
import time

PUMP_PIN = 24  # pin of pump


def run(pin, power, seconds):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
    obj = GPIO.PWM(pin, 100)
    obj.start(0)
    obj.ChangeDutyCycle(power)
    time.sleep(seconds)
    obj.stop()
    GPIO.cleanup()


def turn_on(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)


def turn_off(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


if __name__ == "__main__":
    run(PUMP_PIN, 50, 1)
    print("Pump Start for a second with 50% power")
