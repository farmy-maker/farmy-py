# coding: utf-8
import os
import csv
from apscheduler.scheduler import Scheduler
from datetime import datetime
from modules.light import read_light
from modules.soil_moisture import get_moisture
from modules.soil_temperature import get_celsius
from modules.temperature_and_humidity import get_temperature_and_humidity
from modules.camera import take_picture

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


def fetch_data(path):
    print("Fetch Data {}".format(datetime.now()))
    data = dict(
        light=read_light(),
        soil_moisture=get_moisture(),
        soil_temperature=get_celsius(),
    )
    dht_result = get_temperature_and_humidity()
    if dht_result:
        data.update(dict(
            temperature=dht_result.temperature,
            humidity=dht_result.humidity
        ))
    now = datetime.now()
    data.update(dict(
        ts=int((now - datetime.fromtimestamp(0)).total_seconds()),
        dt=now.strftime("%Y/%m/%d %H:%M:%S")
    ))
    print(data)
    write_data(data, path)
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
    sched.add_cron_job(fetch_data, minute="*/10", args=[path])  # run every 10 minute
    sched.add_cron_job(take_picture, minute="*/30", args=[image_path, camera_type])  # run every 30 minute
    raw_input("Press enter to exit the program\n")
