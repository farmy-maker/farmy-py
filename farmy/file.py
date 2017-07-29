# coding: utf-8
import csv
from datetime import datetime


def write_data(data, path):
    path = path if path.endswith('/') else path + '/'
    with open(path + 'farmy_data.csv', 'a+') as csvfile:
        fieldnames = ['light', 'temperature', 'humidity', 'soil_moisture', 'soil_temperature', 'ts', 'dt']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(data)


def write_image(data, path):
    path = path if path.endswith('/') else path + '/'
    file_name = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    with open(path + file_name, 'wb') as image_file:
        image_file.write(data)
