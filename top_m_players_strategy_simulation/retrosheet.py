#! venv/bin/python 

import urllib
import os

from data import Data as data

class Retrosheet(object):
	"""
	A Retrosheet API to download event files and parse them
	for relevant boxscores

	Data:
		Season: String | Indicates which season's event files this
			object handles (format: yyyy)
		destZipped: String | Indicates where zipped event files go
		destUnzipped: String | Indicates where unzipped event
			files go
		eventFileZipped: String | Path of zipped event file
	"""
	def __init__(self, season, destZipped=data.rootDir + data.defaultDestZippedSuffix, 
					destUnzipped=data.rootDir + data.defaultDestUnzippedSuffix):
		self.season = str(season)
		self.destZipped = destZipped
		self.destUnzipped = destUnzipped
		self.eventFileZipped = self.destZipped + "/r" + self.season + "events.zip"

	def download(self, type='playByPlay'):
		"""
		downloads retrosheet event files for self.season of type type

		type: String | Indicates which type of event file to download 
			(gamelog, play by play, etc)
		"""
		
		if os.path.isfile(eventFileZipped):
			return
		if type == 'playByPlay':
			url = 'http://www.retrosheet.org/events/' + self.season + "eve.zip"
			urllib.urlretrieve(url, filename=eventFileZipped)

	def unzip(self, type='playByPlay'):
		"""
		unzips retrosheet event files for self.season of type type

		type: String | Indicates which type of event file to unzip
			(gamelog, play by play, etc)
		"""
		if !os.path.isfile(self.eventFileZipped):
			self.download()

		# Unzip the file to the unzipped folder
	def get_season(self):
		return self.season

	def get_dest_zipped(self):
		return self.destZipped

	def get_dest_unzipped(self):
		return self.destUnzipped

def main():
	"""
	Short test Suite for Retrosheet
	"""
	## To Teset: Data getters and setters
	r2013 = Retrosheet(2013)

	# Test: download
	r2013.download()
	assert os.path.isfile(r2013.get_dest_zipped() + "/r2013events.zip")

	print "All tests passed!"

if __name__ == "__main__":
	main()
