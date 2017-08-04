# coding: utf-8
import os
import ConfigParser
import argparse
from apscheduler.scheduler import Scheduler
from datetime import datetime

from modules.light import read_light
from modules.soil_moisture import get_moisture
from modules.soil_temperature import get_celsius
from modules.temperature_and_humidity import get_temperature_and_humidity
from modules.controller import Controller
from api import publish_data, publish_image, get_triggers
from output import write_data, write_image

parser = argparse.ArgumentParser(description="Farmy Raspberry Pi Client")
parser.add_argument('--mode', dest='mode', type=str, default='once', help="Set mode. 'hold' or 'once'")
parser.add_argument('--config', dest='config_path', type=str, required=True)

config = ConfigParser.ConfigParser()


def fetch_data(file_path, dht_pin, plant_id, api_key):
    print("Fetch Data {}".format(datetime.now()))
    data = dict(
        light=read_light(),
        soil_moisture=get_moisture(),
        soil_temperature=get_celsius(),
    )
    temperature, humidity = get_temperature_and_humidity(dht_pin)
    if temperature is not None:
        data.update(dict(
            temperature=temperature,
            humidity=humidity
        ))
    now = datetime.now()
    data.update(dict(
        ts=int((now - datetime.fromtimestamp(0)).total_seconds()),
        dt=now.strftime("%Y/%m/%d %H:%M:%S")
    ))
    print(data)
    write_data(data, file_path)
    publish_data(data, plant_id, api_key)


def fetch_image(file_path, camera_type, plant_id, api_key):
    light = read_light()
    if light <= 5:
        print('Too dark to take photo.')
        return
    if camera_type == 'web':
        from modules.camera.webcam import take_picture_web
        image_raw = take_picture_web()
    elif camera_type == 'pi':
        from modules.camera.pi import take_picture_pi
        image_raw = take_picture_pi()
    else:
        raise ValueError("camera_type `{}` invalid".format(camera_type))
    write_image(image_raw, file_path)
    print('Take Picture by {}. Save to {}'.format(camera_type, file_path))
    publish_image(image_raw, plant_id, api_key)


def trigger(pump_pin, led_pin, plant_id, api_key):
    pump_controller = Controller(pump_pin)
    led_controller = Controller(led_pin)
    triggers = get_triggers(plant_id, api_key)
    for trigger_data in triggers:
        action = trigger_data['action']
        if trigger_data['controller'] == 'pump':
            getattr(pump_controller, action)()
        else:
            getattr(led_controller, action)()


def check_device(camera_type):
    if camera_type == "web":
        from modules.camera.webcam import web_camera
        if web_camera is None:
            raise ValueError("web camera not found.")
    elif camera_type == "pi":
        from modules.camera.pi import pi_camera
        if pi_camera is None:
            raise ValueError("Pi Camera not found.")
    else:
        raise ValueError("camera_type `{}` invalid".format(camera_type))


def main():
    args = parser.parse_args()
    mode = args.mode
    config_path = args.config_path
    config.read(config_path)
    camera_type = config.get('device', 'camera_type')
    file_path = config.get('log', 'file_path')
    dht_pin = config.getint('device', 'dht_pin')
    plant_id = config.get('api', 'plant_id')
    api_key = config.get('api', 'api_key')
    pump_pin = config.getint('device', 'pump_pin')
    led_pin = config.getint('device', 'led_pin')

    check_device(camera_type)
    print("Farmy device init.")
    image_path = os.path.join(file_path, 'photos')

    if not os.path.exists(image_path):
        os.makedirs(image_path)

    if mode == 'hold':
        print('Starting...')
        sched = Scheduler()
        sched.start()
        sched.add_cron_job(fetch_data, minute="*/10",
                           args=[file_path, dht_pin, plant_id, api_key])  # run every 10 minute
        sched.add_cron_job(fetch_image, minute="*/10",
                           args=[image_path, camera_type, plant_id, api_key])  # run every 10 minute
        sched.add_cron_job(trigger, minute="*/10",
                           args=[pump_pin, led_pin, plant_id, api_key])  # run every 10 minute

        trigger(pump_pin, led_pin, plant_id, api_key)
        raw_input("Press enter to exit the program\n")
    elif mode == 'once':
        fetch_data(file_path, dht_pin, plant_id, api_key)
        fetch_image(file_path, camera_type, plant_id, api_key)
        trigger(pump_pin, led_pin, plant_id, api_key)
    else:
        print('`--mode` option invalid. `hold` or `once`')


if __name__ == "__main__":
    main()
