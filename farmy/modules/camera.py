#!/usr/bin/python
import argparse
import picamera
from SimpleCV import Camera
from datetime import datetime

DEFAULT_PICTURE_PATH = "/tmp/"

parser = argparse.ArgumentParser()
parser.add_argument('--camera-type', dest='camera_type', type=str, default='web')


web_camera = Camera()


def take_picture_pi(path):
    path = path if path.endswith('/') else path + '/'
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        file_name = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
        camera.capture(path + file_name)


def take_picture_web(path):
    path = path if path.endswith('/') else path + '/'
    img = web_camera.getImage()
    file_name = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    img.save(path + file_name)


def take_picture(path, camera_type):
    if camera_type == 'web':
        take_picture_web(path)
    elif camera_type == 'pi':
        take_picture_pi(path)
    else:
        raise ValueError("camera_type `{}` invalid".format(camera_type))


if __name__ == "__main__":
    args = parser.parse_args()
    camera_type = args.camera_type
    take_picture(DEFAULT_PICTURE_PATH, camera_type)
    print('Take Picture by {}. Save to {}'.format(camera_type, DEFAULT_PICTURE_PATH))
