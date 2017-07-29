FILE_PATH = '/home/pi/farmy'

DHT_PIN = 14  # pin of dht sensor
PUMP_PIN = 24  # pin of pump

CAMERA_TYPE = 'web'  # 'web' or 'pi'

FARMY_HOST = "http://www.farmy.net"
FARMY_USER_PLANT_ENDPOINT = FARMY_HOST + "/api/v0/user_plants/{plant_id}"
FARMY_SENSOR_DATA_ENDPOINT = FARMY_USER_PLANT_ENDPOINT + "/data/"
FARMY_IMAGE_ENDPOINT = FARMY_USER_PLANT_ENDPOINT + "/image/"
FARMY_TRIGGERS_ENDPOINT = FARMY_USER_PLANT_ENDPOINT + "/triggers/"

FARMY_PLANT_ID = "Your Plant ID"
API_KEY = "Your API Key"
