#! venv/bin/python

class Data(object):
	"""
	Holds relevant data that is central to multiple objects

	Purpose: single source of truth
	"""
	rootDir = '/Users/faiyamrahman/programming/Python/beatthestreak' + \
		'/top_m_players_strategy_simulation'
	gl2012Suffix = '/datasets/retrosheet/unzipped/rGamelog2012.txt'
	rIdSuffix = '/datasets/retrosheet/unzipped/rIds.txt'
	defaultDestZippedSuffix = '/datasets/retrosheet/zipped'
	defaultDestUnzippedSuffix = '/datasets/retrosheet/unzipped'