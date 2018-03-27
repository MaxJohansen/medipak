import unittest
from state import State
from dummy import DummySensor


class TestState(unittest.TestCase):
    def test_basics(self):
        fsm = State({'temp': DummySensor([1, 2, 3])})
        fsm.read_sensors()
        self.assertEqual(fsm.readings, [{'temp': 1}])
