#!/usr/bin/python
from SimpleCV import Camera
from datetime import datetime

PICTURE_PATH = "/home/pi/"

camera = Camera()


def take_picture(path=None):
    img = camera.getImage()
    file_name = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    img.save((path or PICTURE_PATH) + file_name)


if __name__ == "__main__":
    print('Take Picture. Save to {}'.format(PICTURE_PATH))
    take_picture()
