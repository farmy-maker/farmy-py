# coding: utf-8
import RPi.GPIO as GPIO
import time

LED_PIN = 23  # pin of led


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
    run(LED_PIN, 50, 1)
    print("Led Start for a second with 50% power")
