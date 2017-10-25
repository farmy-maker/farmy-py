# coding: utf-8
import requests

FARMY_HOST = "https://www.farmy.net"
FARMY_USER_PLANT_ENDPOINT = FARMY_HOST + "/api/v0/user_plants/{plant_id}"
FARMY_SENSOR_DATA_ENDPOINT = FARMY_USER_PLANT_ENDPOINT + "/data/"
FARMY_IMAGE_ENDPOINT = FARMY_USER_PLANT_ENDPOINT + "/image/"
FARMY_TRIGGERS_ENDPOINT = FARMY_USER_PLANT_ENDPOINT + "/triggers/"


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


def get_triggers(plant_id, api_key):
    res = requests.get(FARMY_TRIGGERS_ENDPOINT.format(plant_id=plant_id),
                       headers={"X-Farmy-Api-Key": api_key})
    if not res.ok:
        print(res.content)
    else:
        return res.json()
