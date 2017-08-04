# coding: utf-8
from .trigger import Trigger

PUMP_PIN = 24  # pin of pump


if __name__ == "__main__":
    trigger = Trigger(PUMP_PIN)
    trigger.run(50, 1)
    print("Pump Start for a second with 50% power")
