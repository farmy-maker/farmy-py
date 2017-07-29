# coding: utf-8
import requests

from settings import FARMY_SENSOR_DATA_ENDPOINT, FARMY_IMAGE_ENDPOINT


def publish_data(data, plant_id, api_key):
    res = requests.post(FARMY_SENSOR_DATA_ENDPOINT.format(plant_id=plant_id),
                        data=data,
                        headers={"X-Farmy-Api-Key": api_key})
    if not res.ok:
        print(res.content)


def publish_image(image_raw, plant_id, api_key):
    res = requests.post(FARMY_IMAGE_ENDPOINT.format(plant_id=plant_id),
                        headers={"X-Farmy-Api-Key": api_key},
                        files={'image': image_raw})
    if not res.ok:
        print(res.content)
