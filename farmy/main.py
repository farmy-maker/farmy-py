# coding: utf-8
import os
import csv
import requests
from apscheduler.scheduler import Scheduler
from datetime import datetime
from modules.light import read_light
from modules.soil_moisture import get_moisture
from modules.soil_temperature import get_celsius
from modules.temperature_and_humidity import get_temperature_and_humidity
from modules.camera import take_picture
from settings import PUMP_PIN, DHT_PIN, FARMY_SENSOR_DATA_ENDPOINT, FARMY_TRIGGERS_ENDPOINT, FARMY_PLANT_ID, API_KEY

import argparse

parser = argparse.ArgumentParser(description="Farmy Raspberry Pi Client")
parser.add_argument('--path', type=str)
parser.add_argument('--camera-type', dest='camera_type', type=str)

DEFAULT_PATH = '/home/pi/farmy'
DEFAULT_CAMERA = 'pi'


def write_data(data, path):
    path = path if path.endswith('/') else path + '/'
    with open(path + 'farmy_data.csv', 'a+') as csvfile:
        fieldnames = ['light', 'temperature', 'humidity', 'soil_moisture', 'soil_temperature', 'ts', 'dt']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(data)


def publish_data(data, plant_id, api_key):
    res = requests.post(FARMY_SENSOR_DATA_ENDPOINT.format(plant_id=plant_id),
                        data=data,
                        headers={"X-Farmy-Api-Key": api_key})
    if not res.ok:
        print(res.content)


def fetch_data(path):
    print("Fetch Data {}".format(datetime.now()))
    data = dict(
        light=read_light(),
        soil_moisture=get_moisture(),
        soil_temperature=get_celsius(),
    )
    temperature, humidity = get_temperature_and_humidity(DHT_PIN)
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
    write_data(data, path)
    publish_data(data, FARMY_PLANT_ID, API_KEY)
    return data


if __name__ == "__main__":
    print("Farmy device init.")
    args = parser.parse_args()
    path = args.path or DEFAULT_PATH
    image_path = os.path.join(path, 'photos')
    camera_type = args.camera_type or DEFAULT_CAMERA

    if not os.path.exists(image_path):
        os.makedirs(image_path)

    sched = Scheduler()
    sched.start()
    sched.add_cron_job(fetch_data, second="*/10", args=[path])  # run every 10 minute
    sched.add_cron_job(take_picture, second="*/30", args=[image_path, camera_type])  # run every 30 minute
    raw_input("Press enter to exit the program\n")
