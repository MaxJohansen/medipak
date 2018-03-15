import pycoproc

__version__ = '1.4.0'

print (dir(pycoproc))

class Pytrack(pycoproc.Pycoproc):

    def __init__(self, i2c=None, sda='P22', scl='P21'):
        super().__init__(i2c, sda, scl)
