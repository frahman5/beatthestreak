class Data(object):
    """
    Holds relevant data that is central to multiple objects

    Purpose: single source of truth
    """
    rootDir = '/Users/faiyamrahman/programming/Python/beatthestreak' + \
        '/top_m_players_strategy_simulation'
    rIdSuffix = '/datasets/retrosheet/rId.txt'
    defaultDestZippedSuffix = '/datasets/retrosheet/zipped'
    defaultDestUnzippedSuffix = '/datasets/retrosheet/unzipped'

    @classmethod
    def get_gamelog_path(self, year):
        """
        int -> string
        year: the year for which the user wants the gamelog filepath

        Produces the filepath of the gamelog for year year
        """
        return self.rootDir + '/datasets/retrosheet/unzipped/gamelog' + \
                  str(year) + "/GL" + str(year) + ".TXT"
    
    @classmethod
    def get_event_files_path(self, year):
        """
        int -> string
        year: the year for which the user wants the gamelog filepath

        Produces the filepath of the event files directory for year year
        """
        return self.rootDir + self.defaultDestUnzippedSuffix + \
                   "/events" + str(year)
