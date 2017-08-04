# coding: utf-8
from .trigger import Trigger

LED_PIN = 23  # pin of led


if __name__ == "__main__":
    trigger = Trigger(LED_PIN)
    trigger.run(50, 1)
    print("Led Start for a second with 50% power")
