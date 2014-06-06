class DifficultYearException(Exception):
    pass

class NoPlayerException(Exception):
    pass

class FileContentException(Exception):
	pass

class BadFilepathException(Exception):
	pass

class BadDateException(Exception):
	pass

class NoRetrosheetTypeException(Exception):
	pass

class InvalidResultsMethodException(Exception):
	pass

class NotSuspendedGameException(Exception):
	pass

class SusGameDoesntFitCategoryException(Exception):
	pass

class BotUpdateException(Exception):
	pass