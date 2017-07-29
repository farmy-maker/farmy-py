# coding: utf-8
import os
from apscheduler.scheduler import Scheduler
from datetime import datetime

from modules.camera.pi import take_picture_pi, pi_camera
from modules.camera.webcam import take_picture_web, web_camera
from modules.light import read_light
from modules.soil_moisture import get_moisture
from modules.soil_temperature import get_celsius
from modules.temperature_and_humidity import get_temperature_and_humidity
from api import publish_data, publish_image
from file import write_data, write_image
from settings import FILE_PATH, PUMP_PIN, DHT_PIN, FARMY_PLANT_ID, API_KEY, CAMERA_TYPE


def fetch_data(file_path):
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
    write_data(data, file_path)
    publish_data(data, FARMY_PLANT_ID, API_KEY)


def fetch_image(file_path, camera_type):
    if camera_type == 'web':
        image_raw = take_picture_web()
    elif camera_type == 'pi':
        image_raw = take_picture_pi()
    else:
        raise ValueError("camera_type `{}` invalid".format(camera_type))
    write_image(image_raw, file_path)
    print('Take Picture by {}. Save to {}'.format(camera_type, file_path))
    publish_image(image_raw, FARMY_PLANT_ID, API_KEY)


def check_device(camera_type):
    if camera_type == "web":
        if web_camera is None:
            raise ValueError("web camera not found.")
    elif camera_type == "pi":
        if pi_camera is None:
            raise ValueError("Pi Camera not found.")
    else:
        raise ValueError("camera_type `{}` invalid".format(camera_type))

if __name__ == "__main__":
    check_device(CAMERA_TYPE)
    print("Farmy device init.")
    path = FILE_PATH
    image_path = os.path.join(path, 'photos')

    if not os.path.exists(image_path):
        os.makedirs(image_path)

    sched = Scheduler()
    sched.start()
    sched.add_cron_job(fetch_data, minute="*/10", args=[path])  # run every 10 minute
    sched.add_cron_job(fetch_image, minute="*/10", args=[image_path, CAMERA_TYPE])  # run every 10 minute
    raw_input("Press enter to exit the program\n")
