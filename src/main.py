# import time
import utime
import json
import pycom
import math
from colors import WHITE, GREEN, YELLOW, RED
from pytrack import Pytrack
from L76GNSS import L76GNSS
from LIS2HH12 import LIS2HH12
from startiot import Startiot

py = Pytrack()
gps = L76GNSS(py, timeout=10)
acc = LIS2HH12()

speed_readings = 0

# disable the blue blinking
pycom.heartbeat(False)

iot = Startiot()
pycom.rgbled(0xFF0000)
iot.connect()
pycom.rgbled(WHITE)


def get_speed():
    global speed_readings
    speed_readings += 1
    return round(math.sqrt(sum(x**2 for x in acc.acceleration())), 1)


def get_code(severity):
    if 0 <= severity < 4:
        return 'green'
    elif 4 <= severity < 8:
        return 'yellow'
    elif 8 <= severity:
        return 'red'


severity = 0
count = 1

while not py.button_pressed():
    utime.sleep_ms(100)

speed = get_speed()
colors = {
    'red': RED,
    'yellow': YELLOW,
    'green': GREEN
}

while True:
    data = {}
    new_speed = get_speed()
    if new_speed > speed:
        severity = min(severity + 1, 10)
    else:
        severity = max(severity - 0.2, 0)

    speed = new_speed

    print('Severity:', severity)
    pycom.rgbled(colors[get_code(severity)])
    if speed_readings == 10:
        data['count'] = count
        data['severity'] = round(severity, 1)
        data['code'] = get_code(severity)

        coords = gps.coordinates()
        if coords[0]:
            data['latlng'] = "{},{}".format(coords[0], coords[1])

        payload = json.dumps(data)
        print('Sending: ', payload)
        iot.send(payload)
        print('Data sent...')
        count = count + 1
        speed_readings = 0

    utime.sleep(1)
