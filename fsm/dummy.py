class DummySensor(object):
    def __init__(self, readings):
        self.readings = iter(readings)
        self.num_reads = 0

    def read(self, failure=False):
        if failure:
            raise Exception('placeholder exception')

        self.num_reads += 1
        try:
            return next(self.readings)
        except StopIteration:
            return False
