import time
import RPi.GPIO as GPIO
from dht11 import DHT11

DHT_PIN = 14


def _get_temperature_and_humidity():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    instance = DHT11(pin=DHT_PIN)
    result = instance.read()
    GPIO.cleanup()
    if result.is_valid():
        return result


def get_temperature_and_humidity():
    for retry in range(100):
        time.sleep(0.05)
        result = _get_temperature_and_humidity()
        if result:
            return round(result.temperature, 3), round(result.humidity, 3)
    return None, None


if __name__ == "__main__":
    while True:
        temperature, humidity = get_temperature_and_humidity()
        if temperature:
            print("Temperature: {}C".format(temperature))
            print("Humidity: {}%".format(humidity))
            time.sleep(3)
