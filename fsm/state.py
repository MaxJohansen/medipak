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
			self.read_sensors()
			self.send_payload()
			self.wait()
			self.next()

	def read_sensors(self):
		"""Appends a new set of sensor readings
		to a list of dictionaries where the keys
		are strings of the data-name and values
		are the actual readings from the given
		sensors."""
		self.readings.append({name: sensor.read() for name, sensor in self.sensors})

	def send_payload(self):
		print('Sending payload')

	def analyse(self, x):
		"""Looks at the x latest readings and
		analyses each to determine if the state
		should change"""
		print('Analysing data...')

	def next(self):
		"""Analyse data and move to next state
		if needed."""
		print('Moving to next state, maybe...')
