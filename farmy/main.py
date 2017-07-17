# coding: utf-8
import csv
from datetime import datetime
from modules.light import read_light
from modules.soil_moisture import get_moisture
from modules.soil_temperature import get_celsius
from modules.temperature_and_humidity import get_temperature_and_humidity
from modules.webcamera import take_picture
from apscheduler.scheduler import Scheduler


CSV_PATH = '/home/pi/'


def write_data(data):
    with open(CSV_PATH + 'farmy_data.csv', 'a') as csvfile:
        fieldnames = ['light', 'temperature', 'humidity', 'soil_moisture', 'soil_temperature', 'ts', 'dt']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(data)


def fetch_data():
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
    write_data(data)
    return data


if __name__ == "__main__":
    print("Farmy device init.")
    sched = Scheduler()
    sched.start()
    # sched.add_cron_job(fetch_data, second="*/10")  # run every 10 seconds
    sched.add_cron_job(fetch_data, minute="*/10")  # run every 10 minute
    sched.add_cron_job(take_picture, minute="*/30")  # run every 30 minute
    data = fetch_data()
    raw_input("Press enter to exit the program\n")
