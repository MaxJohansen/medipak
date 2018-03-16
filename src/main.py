# import time
import utime
import json
import machine
import pycom
import math
from colors import color
from pytrack import Pytrack
from L76GNSS import L76GNSS
from LIS2HH12 import LIS2HH12
from startiot import Startiot

# disable the blue blinking
pycom.heartbeat(False)

iot = Startiot()
pycom.rgbled(0xFF0000)
iot.connect()
pycom.rgbled(0xFFFFFF)

rtc = machine.RTC()
rtc.ntp_sync('pool.ntp.org')
utime.sleep_ms(750)
print('\nRTC set from NTP to UTC:', rtc.now())
utime.timezone(7200)
print('adjusted from UTC to EST timezone', utime.localtime(), '\n')
py = Pytrack()
gps = L76GNSS(py, timeout=10)
accelerometer = LIS2HH12()

count = 1

while True:
    data = {}
    coords = gps.coordinates()
    if coords[0]:
        data['latlng'] = "{},{}".format(coords[0], coords[1])

    acc = accelerometer.acceleration()
    speed = math.sqrt(sum(x**2 for x in acc))
    data['speed'] = speed
    data['count'] = count
    payload = json.dumps(data)
    print("Sending: ", payload)
    count = count + 1

    # send some data
    iot.send(payload)
    print("Data sent...")

    pycom.rgbled(next(color))
    utime.sleep(10)
