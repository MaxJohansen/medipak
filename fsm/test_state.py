import unittest
from state import State
from dummy import DummySensor


class TestState(unittest.TestCase):
    def setUp(self):
        self.temp_sensor = DummySensor([37, 38, 39])
        self.hr_sensor = DummySensor([100, 110, 90])
        self.all_sensors = {'temp': self.temp_sensor,
                            'heartrate': self.hr_sensor}

    def test_reads_from_sensor(self):
        fsm = State({'temp': self.temp_sensor})
        fsm.run_one_cycle()
        self.assertEqual(self.temp_sensor.num_reads, 1)
        self.assertEqual(fsm.readings, [{'temp': 37}])

    def test_reads_from_all_sensors(self):
        fsm = State(self.all_sensors)
        fsm.run_one_cycle()
        for stat, sensor in self.all_sensors.items():
            self.assertEqual(sensor.num_reads, 1, stat)

    def test_prepares_payload(self):
        fsm = State({'temp': self.temp_sensor})
        fsm.run_one_cycle()
        fsm.run_one_cycle()
        fsm.run_one_cycle()
        self.assertDictEqual(fsm.payload, {'temp': 38.0})
