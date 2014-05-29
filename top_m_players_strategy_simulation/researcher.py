import os
import re

from datetime import date
from data import Data
from utilities import Utilities
from retrosheet import Retrosheet

class Researcher(object):
    """
    A MLB researcher. His main function is to look up 
    facts about MLB events (games, seasons, teams, etc) that
    are not specific to any one player
    """

    def get_participants(self, date):
        """
        date(year, month, day) -> ListOfStrings
        date: a date of the year

        Produces a list of retrosheet ids corresponding to players starting, 
        umps officiating, and managers managing on the given day
        """
        year = date.year
        dateRFormat = Utilities.convert_date(date) # date in yyyymmdd format
        gamelogPath = Data.rootDir + Data.defaultDestUnzippedSuffix + \
                            "/gamelog" + str(year) + "/GL" + str(year) + ".TXT"

        # Makesure the gamelog is on the drive
        if not os.path.isfile(gamelogPath): 
            rsheet = Retrosheet(year)
            rsheet.download(type='gamelog')
            rsheet.unzip(type='gamelog')
            
        #extract all the games on the given date
        with open(gamelogPath, "r") as f:
            list_of_games = [line.replace('"', '').split(',')[1:]
                                    for line in f if dateRFormat in line]

        # get the retrosheet ids from the games
        p = re.compile("[a-z]{5}[0-9]{3}")
        return [field for game in list_of_games
                    for field in game if re.match(p, field)]

