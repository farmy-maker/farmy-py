# farmy-py
Python SDK for [Farmy](https://www.farmy.net/)

### Raspberry Pi Configuration
```
pi@raspberrypi:~ $ sudo raspi-config
```
Interfacing Options > 
Enable Camera, I2C, 1-Wire.

### Installation

#### Requirements
```
pi@raspberrypi:~ $ sudo apt-get install python-pip python-dev python-opencv python-scipy git
```

#### Download Source code
```
pi@raspberrypi:~ $ cd /home/pi
pi@raspberrypi:~ $ git clone https://github.com/farmy-maker/farmy-py.git
pi@raspberrypi:~ $ cd farmy-py
pi@raspberrypi:~/farmy-py $
```

#### Installation
```
pi@raspberrypi:~ $ pip install -r requirements.txt
```

### Usage

#### Configuration
Edit config.ini

```
[api]
plant_id = Your Plant ID    # Plant ID in www.farmy.net 
api_key = Your API Key      # API Key issued by www.farmy.net

[device]
camera_type = web           # 'web' when using webcam and "pi" when using pi camera
dht_pin = 14                # pin of dht11 sensor
led_pin = 23                # pin of led
pump_pin = 24               # pin of pump

[log]
file_path = /home/pi/farmy  # log file in raspberry pi
```

#### Running

```
pi@raspberrypi:~/farmy-py $ farmy.py --config ./config.ini
Farmy Device Init.
Date Receivced. {}
Picture Captured. Saved to /home/pi/farmy/photos
```

##### Running as service

```
pi@raspberrypi:~/farmy-py $ farmy.py --config ./config.ini --mode=hold
```

