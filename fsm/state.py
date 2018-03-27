from enum import Enum


class Color(Enum):
    WHITE = 0
    GREEN = 1
    YELLOW = 2
    RED = 3


class State():
    def __init__(self, sensors):
        self.state = Color.WHITE
        self.wait_time = 60
        self.sensors = sensors
        self.readings = list()

    def start(self):
        """Runs the state-machine in a loop,
        gouverning its own send-frequency."""
        while True:
            self.loop()

    def loop(self):
        self.read_sensors()
        self.analyse()
        self.send_payload()
        self.wait()

    def read_sensors(self):
        """Appends a new set of sensor readings
        to a list of dictionaries where the keys
        are strings of the data-name and values
        are the actual readings from the given
        sensors."""
        self.readings.append({name: sensor.read()
                              for name, sensor in self.sensors.items()})
        while len(self.readings) > 10:
            self.readings = self.readings[1:]

    def wait(self):
        print('waiting for {self.wait_time}'.format(self=self))

    def send_payload(self):
        print('Sending payload')

    def analyse(self):
        """Looks at the x latest readings and
        analyses each to determine if the state
        should change"""
        allvals = {}
        for reading in self.readings:
            for key, value in reading.items():
                if key in allvals:
                    allvals[key].append(value)
                else:
                    allvals[key] = [value]

        averages = {key: sum(vals) / len(vals)
                    for key, vals in allvals.items()}
        print('Analysing data...', averages)


if __name__ == '__main__':
    from dummy import DummySensor
    ds = DummySensor([37.1, 37.2, 37.0, 37.5, 37.8,
                      37.3, 38.0, 38.3, 38.6, 39.0])
    fsm = State({'temp': ds})
    for _ in range(10):
        fsm.loop()
