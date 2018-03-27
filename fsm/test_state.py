import unittest
from state import State
from dummy import DummySensor


class TestState(unittest.TestCase):
    def test_reads_from_sensor(self):
        temp_sensor = DummySensor([1, 2, 3])
        fsm = State({'temp': temp_sensor})
        fsm.run_one_cycle()
        self.assertEqual(temp_sensor.num_reads, 1)
        self.assertEqual(fsm.readings, [{'temp': 1}])

    def test_reads_from_all_sensors(self):
        temp_sensor = DummySensor([])
        hr_sensor = DummySensor([])
        fsm = State({'temp': temp_sensor, 'heartrate': hr_sensor})
        fsm.run_one_cycle()
        self.assertEqual(temp_sensor.num_reads, 1)
        self.assertEqual(hr_sensor.num_reads, 1)
