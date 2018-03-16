# import time
import utime
import json
import machine
import pycom
from pytrack import Pytrack
from L76GNSS import L76GNSS
from startiot import Startiot

# disable the blue blinking
pycom.heartbeat(False)

iot = Startiot()
pycom.rgbled(0xFF0000)
iot.connect()
pycom.rgbled(0x0000FF)
print('iot connected')

pycom.rgbled(0xf0f011)

rtc = machine.RTC()
rtc.ntp_sync('pool.ntp.org')
utime.sleep_ms(750)
print('\nRTC set from NTP to UTC:', rtc.now())
utime.timezone(7200)
print('adjusted from UTC to EST timezone', utime.localtime(), '\n')
py = Pytrack()
gps = L76GNSS(py, timeout=30)
chrono = machine.Timer.Chrono()
chrono.start()

count = 0
while True:
    data = {}
    coords = gps.coordinates()
    if coords[0]:
        data['latlng'] = "{}, {}".format(coords[0], coords[1])
    data['count'] = count
    payload = json.dumps(data)
    print("Sending data... ", payload)
    count = count + 1

    # send some data
    iot.send(payload)
    pycom.rgbled(0x00ff00)
    utime.sleep(0.1)
    pycom.rgbled(0x000000)
    utime.sleep(0.1)
    pycom.rgbled(0x00ff00)
    utime.sleep(0.1)
    pycom.rgbled(0x000000)
    print("Data sent...")

    # get any data received
    data = iot.recv(64)
    print("Received Data:", data)

    utime.sleep(30)
