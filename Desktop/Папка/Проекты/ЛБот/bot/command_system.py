command_list = []

class Command:

	def __init__(self):

		self.need_parameter = False
		self._keys = []
		self.description = ''
		command_list.append(self)

	@property
	def keys(self):
		return self._keys


	@keys.setter
	def keys(self, mas):
		for k in mas:
			self._keys.append(k.lower())

	def process(self):
		pass