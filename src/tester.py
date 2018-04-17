import utime
from max30102 import MAX30102

maxim = MAX30102()

print("Reading maxim sensor")

while True:
    maxim.read_fifo()
    utime.sleep(2)
