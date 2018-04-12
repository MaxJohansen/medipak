from enum import Enum
import json


class Color(Enum):
    WHITE = 0
    GREEN = 1
    YELLOW = 2
    RED = 3


class State():
    def __init__(self, sensors):
        """A Finite State Machine for the MedPack

        :param sensors: A dict of str -> Sensor
        """
        self.readings = list()
        self.sensors = sensors
        self.state = Color.WHITE
        self.wait_time = 60
        self.payload = ""

    def loop(self):
        """Runs the state - machine in a loop."""
        while True:
            self.run_one_cycle()

    def run_one_cycle(self):
        """A single cycle:
        - Reads all sensors and appends readings to the list
        - Analyses the readings, changing state if necessary
        - Sends payload to backend
        - Waits until it is time to send another payload"""
        self.read_sensors()
        self.analyse()
        self.send_payload()
        self.wait()

    def read_sensors(self):
        """Appends a new set of sensor readings
        to a list of dictionaries where the keys
        are strings of the data - name and values
        are the actual readings from the given
        sensors."""
        new_readings = {name: sensor.read()
                        for name, sensor in self.sensors.items()}
        new_readings = {name: value for name,
                        value in new_readings.items() if value}
        self.readings.append(new_readings)
        while len(self.readings) > 10:
            self.readings = self.readings[1:]

    def wait(self):
        print('Stub: waiting for {self.wait_time}'.format(self=self))

    def send_payload(self):
        print('Stub: sending payload:', json.dumps(self.payload))

    def analyse(self):
        """Analyses the average of all readings
        to determine if the state should change"""
        allvals = {}
        for reading in self.readings:
            for key, value in reading.items():
                if key in allvals:
                    allvals[key].append(value)
                else:
                    allvals[key] = [value]

        averages = {key: sum(vals) / len(vals)
                    for key, vals in allvals.items()}
        print('Stub: analysing data...')
        self.payload = averages


if __name__ == '__main__':
    from dummy import DummySensor
    ds = DummySensor([37.1, 37.2, 37.0, 37.5, 37.8,
                      37.3, 38.0, 38.3, 38.6, 39.0])
    fsm = State({'temp': ds})
    for _ in range(20):
        fsm.run_one_cycle()
