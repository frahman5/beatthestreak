import os
import re

from datetime import date
from data import Data
from utilities import Utilities
from retrosheet import Retrosheet

class Researcher(object):
    """
    A MLB researcher. His main function is to look up 
    facts about MLB events (games, seasons, teams, etc)
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

    def find_home_team(self, date, player):
        """
        date(year, month, day) Player -> String
        date: a date in the year during the MLB season
        Player: a player participating in a game on the given date

        Produces a three digit abbreviation for the home team that played
            a game involving given player on given date
        """
        year = date.year
        date = Utilities.convert_date(date)
        
        if not os.path.isfile(Data.get_gamelog_path(year)):
            r = Retrosheet(year)
            r.download_and_unzip(type='gamelog')

        with open(Data.get_gamelog_path(year), "r") as f:
            list_of_games = [line.replace('"', '').split(',')
                                    for line in f if date in line]
        homeTeamList = [game[6] for game in list_of_games 
                           if player.get_retrosheet_id() in game]
        return homeTeamList[0]

    def did_start(self, date, player):
        """
        date: datetime.date(year, month, day) | a date in the year

        Returns: Boolean | True if player started a game on the given date, False otherwise
        """
        return player.get_retrosheet_id() in self.get_participants(date)

    def did_get_hit(self, date, player):
        """
        date(year, month, day) Player -> Boolean

        date: a date in the year
        player: an MLB player

        Produces True if player got a hit on the given date, False otherwise 
        """
        # os.chdir(Data.get_event_files_path(date.year))
        team = self.find_home_team(date, player) # need home team's box score
        boxscore = Data.get_event_files_path(date.year) + "/" + str(date.year) + \
                      team + "B.txt"
        lastName = player.get_last_name()
        firstName = player.get_first_name()

        # Ensure that necessary retrosheet files are present
        if not os.path.isfile(boxscore):
            r = Retrosheet(date.year)
            r.gen_boxscores()
        
        with open(boxscore, "r") as file: 
            line = ""

            # find this date's game's boxscore
            search = str(date.month) + "/" + str(date.day) + "/" + str(date.year)
            while search not in line: line = file.readline()

            # find this player's line in the boxscore
            search = lastName + " " + firstName[0]
            while search not in line: line = file.readline()

            #find the index of this player's last name in the line
            info = line.split()
            index = info.index(lastName)
            if info[index + 1] != firstName[0] + ",":
                print "We had two lined up players with same last name!" 
                print "Here's the line: %s" % (str(line))
                index = info[index + 1:].index(lastName)

            # Player's hit count is 5 off his last name. 
            return int(info[index+5]) > 0

        #Make it work for a player who got traded. Test MUCH more robustly. 

