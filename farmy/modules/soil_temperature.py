# -*- coding: utf-8 -*-
from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()


def get_celsius():
    return sensor.get_temperature()


if __name__ == "__main__":
    temperature = sensor.get_temperatures()
    print("Celsius: {0:.3f}".format(temperature))
