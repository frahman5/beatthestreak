class DifficultYearException(Exception):
	def __init__(self, errorMessage):
		self.errorMessage = errorMessage
	def __str__(self):
		return repr(self.errorMessage)

class NoPlayerException(Exception):
	def __init__(self, errorMessage):
		self.errorMessage = errorMessage
	def __str__(self):
		return repr(self.errorMessage)