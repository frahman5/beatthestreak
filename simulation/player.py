import os
import pandas as pd
import numpy as np

from datetime import date
from data import Data
from utilities import Utilities
from researcher import Researcher
from retrosheet import Retrosheet

class Player(object):
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
    """
    
    def __init__(self, index, first_n, last_n, bat_ave_year):
        self.index = index
        self.first_name = first_n
        self.last_name = last_n
        self.rId = self.__set_retrosheet_id()
        self.lId = self.__set_lahman_id()
        self.bat_ave = self.__set_bat_ave(bat_ave_year)

    def __set_retrosheet_id(self):
        """
        Returns: string | retrosheet id of player
            If player name has multiple ids, prompts user to choose one
        """
        name = self.last_name + "," + self.first_name
        
        # Get list of possible ids
        with open(Data.get_retrosheet_id_path(), "r") as f:
            possible_ids = [line.split(',')[2] for line in f if name in line]

        # Choose appropriate id
        if len(possible_ids) == 1: return possible_ids[0]
        else:
            x = ""
            while x not in possible_ids:
                print ""
                if x is not "": print "You mistyped. Please Try Again"
                print "Multiple ids found: "
                for id in possible_ids: print id
                print "Choose one. Reference rId.txt if you are unsure."
                x = str(raw_input())
            return x
        
    def get_retrosheet_id(self):
        return self.rId

    def __set_lahman_id(self):
        df = pd.read_csv(Data.get_lahman_path("master"), 
                         usecols=["playerID", "retroID"])
        
        # Chop the dataframe with retroId == self.rId, then get the 
        # lone item remaining in column playerID
        return df[df.retroID == self.rId]['playerID'].item()


    def get_lahman_id(self):
        return self.lId

    def __set_bat_ave(self, year):
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
    
    def get_index(self):
        return self.index
    
    def get_name(self):
        return self.first_name + " " + self.last_name

    def get_last_name(self):
        return self.last_name

    def get_first_name(self):
        return self.first_name
    

