import os
import pandas as pd

from datetime import date, datetime
from utilities import Utilities
from retrosheet import Retrosheet
from exception import NoPlayerException
from researcher import Researcher
from filepath import Filepath

class PlayerL(object):
    """
    An MLB athlete with limited data.
    Data:
        lId: string | player's lahman id
        bat_ave: [float[0,1]] | player's batting average for some year

    Purpose: Batting averages must be calculated often, but you don't need
    a full blown player to do that. This object houses the batting average
    calculation methods without the extra fluff
    """

    def __init__(self, lahmanID, bat_ave_year):
        self.lId = lahmanID
        self.bat_ave = self._set_bat_ave(bat_ave_year)
 
    def _set_bat_ave(self, year):
        """
        int -> float
        year: a year as a 4 digit int

        Produces the season batting average of self in year year, rounded
        off to 3 decimal places
        """
        # Read in relevant columns from batting.csv
        df = pd.read_csv(Filepath.get_lahman_file("batting"), 
                         usecols=['playerID', 'yearID', 'AB', 'H'])

        # Getting batting stats for player in given year
        batting_stats_df = df[df.playerID == self.lId][df.yearID == year]

        # Sum over all the hits and divide by the sum over all at-bats
        #   accounts for players who were traded mid season via summing
        return round(sum(batting_stats_df.H) / sum(batting_stats_df.AB), 3)

    def get_bat_ave(self):
        return self.bat_ave

    def get_lahman_id(self):
        return self.lId

class Player(PlayerL):
    """
    A player representing a MLB athlete.
    Filepath.
        index: int[>=0] | player index in a simulation
        rId: string | player's retrosheet id
        lId: string | player's lahman id
        first_name: string | Player's first name
            -> must capitalize first letter
        last_name: string | Player's last name
            -> must capitalize first letter
        bat_ave: float[0, 1] | player's batting average
        debut: string(mm/dd/yyyy) | date of player's debut
    """
    
    def __init__(self, *args, **kwargs):
        """
        Can construct in multiple ways:
        1) Player(index, firstN, lastN, batAveYear)
            -> constructor will find retrosheet id, lahman id, batting ave, and
            if necessary prompt the user for a debut date
        2) Player(index, firstN, lastN, batAveYear, debut='mmddyyy')
            -> same as above, except now with player debut date specified, 
            there is almost no chance of ambiguity in retrieving a retrosheet id
        3) Player(index, playerL = *playerLInstance*)
            -> takes lahmanID and batting ave from lahmanId. 
            Obtains name, and retrosheet_id on its own
        """
        # Type 3
        if 'playerL' in kwargs.keys():
            assert len(args) == 1
            self.__init__from_playerL(args[0], kwargs['playerL'])
            return

        # Types 1 and 2
        assert len(args) == 4
        if 'debut' in kwargs.keys():
            self.debut = kwargs['debut']
        else:
            self.debut = None
        self.index = args[0]
        self.first_name = args[1]
        self.last_name = args[2]
        self.rId = self.__set_retrosheet_id(source='name')
        self.lId = self.__set_lahman_id()
        self.bat_ave = self._set_bat_ave(args[3])

    def __init__from_playerL(self, index, playerL):
        """
        playerL -> None

        helper function for init. Initalizes the instance from a playerL
        instance
        """
        self.index = index
        self.lId = playerL.get_lahman_id()
        self.first_name, self.last_name = Researcher.name_from_lahman_id(self.lId)
        self.rId = self.__set_retrosheet_id(source='lahmanID')
        self.bat_ave = playerL.get_bat_ave()

    def __eq__(self, other):
        # technically, only need one. but dependability via redundancy :)
        samerId = (self.rId == other.get_retrosheet_id())
        samelId = (self.lId == other.get_lahman_id())
        return samerId and samelId

    def __str__(self):
        return self.get_name() + ": %.3f" % self.bat_ave

    def __repr__(self):
        return self.__str__()

    def __set_retrosheet_id(self, source='name'):
        """
        Returns: string | retrosheet id of player
        """
        if source == 'name':
            return self.fetch_retrosheet_id_from_name()
        if source == 'lahmanID':
            return self.fetch_retrosheet_id_from_lahman_ID()

    def fetch_retrosheet_id_from_name(self):
        df = pd.read_csv(Filepath.get_retrosheet_file(folder='base', fileF='id'))
        df = df[df.FIRST == self.first_name][df.LAST == self.last_name]

        if len(df) == 0:
            raise NoPlayerException("No player found with name %s" % \
                    self.first_name + " " + self.last_name)
        if len(df) == 1:
            return df.ID.item()
        # else len(df) > 1
        i = 0
        while self.debut not in df.DEBUT.values:
            if i > 0: print "\nYou mistyped. Try again"
            print "\nMultiple ids found. What was " + \
                "%s's debut date? Options:" % self.get_name()
            for debut in df.DEBUT: print debut
            self.debut = str(raw_input())
            i += 1

        for debut in df.DEBUT:
            if datetime.strptime(debut, '%m/%d/%Y') == \
                 datetime.strptime(self.debut, '%m/%d/%Y'):
                return df[df.DEBUT == debut].ID.item()

    def fetch_retrosheet_id_from_lahman_ID(self):
        df = pd.read_csv(Filepath.get_lahman_file("master"), 
                usecols=['playerID', 'retroID'])
        return df[df.playerID == self.lId].retroID.item()
        
    def get_retrosheet_id(self):
        return self.rId

    def __set_lahman_id(self):
        df = pd.read_csv(Filepath.get_lahman_file("master"), 
                         usecols=["playerID", "retroID"])
        
        # Chop the dataframe with retroId == self.rId, then get the 
        # lone item remaining in column playerID
        return df[df.retroID == self.rId]['playerID'].item()
    
    def set_index(self, index):
        self.index = index

    def get_index(self):
        return self.index
    
    def get_name(self):
        return self.first_name + " " + self.last_name

    def get_last_name(self):
        return self.last_name

    def get_first_name(self):
        return self.first_name



