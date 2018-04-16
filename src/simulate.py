# import time
import utime
import json
import pycom
import math
from colors import WHITE, GREEN, YELLOW, RED
from startiot import Startiot

readings = [
    {'hr': 77, 'temp': 36.6, 'SpO2': 96.7, 'latlng': "69.68141, 18.97231"},
    {'hr': 80, 'temp': 36.8, 'SpO2': 96.8, 'latlng': "69.68141, 18.97231"},
    {'hr': 76, 'temp': 36.7, 'SpO2': 96.8, 'latlng': "69.68141, 18.97231"},
    {'hr': 76, 'temp': 37.0, 'SpO2': 96.9, 'latlng': "69.68141, 18.97231"},
    {'hr': 77, 'temp': 37.2, 'SpO2': 97.1, 'latlng': "69.68141, 18.97231"},
    {'hr': 78, 'temp': 37.3, 'SpO2': 97.1, 'latlng': "69.68141, 18.97231"},
    {'hr': 80, 'temp': 37.1, 'SpO2': 97.0, 'latlng': "69.68141, 18.97231"},
    {'hr': 79, 'temp': 37.2, 'SpO2': 96.8, 'latlng': "69.68141, 18.97231"},
    {'hr': 80, 'temp': 37.0, 'SpO2': 96.7, 'latlng': "69.68141, 18.97231"},
    {'hr': 79, 'temp': 36.8, 'SpO2': 96.6, 'latlng': "69.68141, 18.97231"},
    {'hr': 76, 'temp': 36.9, 'SpO2': 95.8, 'latlng': "69.68141, 18.97231"},
    {'hr': 77, 'temp': 36.7, 'SpO2': 96.2, 'latlng': "69.68141, 18.97231"},
    {'hr': 78, 'temp': 36.6, 'SpO2': 96.3, 'latlng': "69.68141, 18.97231"},
    {'hr': 78, 'temp': 36.7, 'SpO2': 97.0, 'latlng': "69.68141, 18.97231"},
    {'hr': 79, 'temp': 37.0, 'SpO2': 96.7, 'latlng': "69.68141, 18.97231"},
    {'hr': 81, 'temp': 36.9, 'SpO2': 96.8, 'latlng': "69.68141, 18.97231"},
    {'hr': 78, 'temp': 36.8, 'SpO2': 96.7, 'latlng': "69.68141, 18.97231"},
    {'hr': 78, 'temp': 36.9, 'SpO2': 96.5, 'latlng': "69.68141, 18.97231"},
    {'hr': 77, 'temp': 36.9, 'SpO2': 97.0, 'latlng': "69.68141, 18.97231"},
    {'hr': 82, 'temp': 37.0, 'SpO2': 97.4, 'latlng': "69.68141, 18.97231"},
    {'hr': 81, 'temp': 37.2, 'SpO2': 97.5, 'latlng': "69.68141, 18.97231"},
    {'hr': 79, 'temp': 37.1, 'SpO2': 97.6, 'latlng': "69.68141, 18.97231"},
    {'hr': 77, 'temp': 37.0, 'SpO2': 97.6, 'latlng': "69.68141, 18.97231"},
]

# disable the blue blinking
pycom.heartbeat(False)

iot = Startiot()
pycom.rgbled(0xFF0000)
iot.connect()
pycom.rgbled(WHITE)

count = 1

colors = {
    'red': RED,
    'yellow': YELLOW,
    'green': GREEN
}

for data in readings:
    data['count'] = count
    count = count + 1

    payload = json.dumps(data)
    print('Sending: ', payload)
    iot.send(payload)
    utime.sleep(30)
    print('Data sent...')
