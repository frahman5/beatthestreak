import os
import pandas as pd

from datetime import date, datetime
from data import Data
from utilities import Utilities
from retrosheet import Retrosheet
from exception import NoPlayerException

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
        df = pd.read_csv(Data.get_lahman_path("batting"), 
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
    Data:
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
    
    def __init__(self, index, first_n, last_n, bat_ave_year, **kwargs):
        if 'debut' in kwargs.keys():
            self.debut = kwargs['debut']
        else:
            self.debut = None
        self.index = index
        self.first_name = first_n
        self.last_name = last_n
        self.rId = self.__set_retrosheet_id()
        self.lId = self.__set_lahman_id()
        self.bat_ave = self._set_bat_ave(bat_ave_year)

    def __set_retrosheet_id(self):
        """
        Returns: string | retrosheet id of player
        """
        df = pd.read_csv(Data.get_retrosheet_id_path())
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
            print "\nMultiple ids found. What was player's debut date? Options:"
            for debut in df.DEBUT: print debut
            self.debut = str(raw_input())
            i += 1

        for debut in df.DEBUT:
            if datetime.strptime(debut, '%m/%d/%Y') == \
                 datetime.strptime(self.debut, '%m/%d/%Y'):
                return df[df.DEBUT == debut].ID.item()
        
    def get_retrosheet_id(self):
        return self.rId

    def __set_lahman_id(self):
        df = pd.read_csv(Data.get_lahman_path("master"), 
                         usecols=["playerID", "retroID"])
        
        # Chop the dataframe with retroId == self.rId, then get the 
        # lone item remaining in column playerID
        return df[df.retroID == self.rId]['playerID'].item()
    
    def get_index(self):
        return self.index
    
    def get_name(self):
        return self.first_name + " " + self.last_name

    def get_last_name(self):
        return self.last_name

    def get_first_name(self):
        return self.first_name



