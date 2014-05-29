##### BEFORE SIMULATING, need to adjust this to be able to handle any year. 
##### Currently only works for 2012
import os

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
        id: string | retrosheet id for player
        first_name: string | Player's first name
            -> must capitalize first letter
        last_name: string | Player's last name
            -> must capitalize first letter
        bat_ave: float[0, 1] | player's batting average
    """
    
    def __init__(self, index, first_n, last_n, bat_ave, year):
        self.index = index
        self.first_name = first_n
        self.last_name = last_n
        self.id = self.set_retrosheet_id()
        self.bat_ave = bat_ave

    def set_retrosheet_id(self):
        """
        Returns: string | retrosheet id of player
            If player name has multiple ids, prompts user to choose one
        """
        name = self.last_name + "," + self.first_name
        
        # Get list of possible ids
        with open(Data.get_retrosheet_id_path, "r") as f:
            possible_ids = [line.split(',')[2] for line in f if name in line]

        # Choose appropriate id
        if len(possible_ids) == 1:
            return possible_ids[0]
        else:
            x = ""
            while x not in possible_ids:
                print "Multiple ids found: "
                for id in possible_ids: print id
                print "Choose one."
                x = str(raw_input())
            return x
        
    def get_retrosheet_id(self):
        return self.id
    
    def get_index(self):
        return self.index
    
    def get_name(self):
        return self.first_name + " " + self.last_name

    def get_last_name(self):
        return self.last_name

    def get_first_name(self):
        return self.first_name
    
    def get_bat_ave(self):
        return self.bat_ave
