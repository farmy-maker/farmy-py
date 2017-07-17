import time
import RPi.GPIO as GPIO
from dht11 import DHT11

DHT_PIN = 14
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


def _get_temperature_and_humidity():
    instance = DHT11(pin=DHT_PIN)
    result = instance.read()
    if result.is_valid():
        return result


def get_temperature_and_humidity():
    for retry in range(3):
        time.sleep(0.1)
        result = _get_temperature_and_humidity()
        if result:
            return result


if __name__ == "__main__":
    while True:
        result = get_temperature_and_humidity()
        if result:
            print("Temperature:" + str(result.temperature) + " C")
            print("Humidity:" + str(result.humidity) + "%")
            time.sleep(3)
