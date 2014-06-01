import os
import re
import pandas as pd

from datetime import date
from data import Data
from utilities import Utilities
from retrosheet import Retrosheet

class Researcher(object):
    """
    A MLB researcher. His main function is to look up 
    facts about MLB events (games, seasons, teams, etc)
    """
    @classmethod
    def get_participants(self, date):
        """
        date(year, month, day) -> ListOfStrings
        date: a date of the year

        Produces a list of retrosheet ids corresponding to players starting, 
        umps officiating, and managers managing on the given day
        """
        dateRFormat = Utilities.convert_date(date) # date in yyyymmdd format
        gamelogPath = Data.get_unzipped_gamelog_path(date.year)

        # Make sure the gamelog is on the drive
        if not os.path.isfile(gamelogPath): 
            rsheet = Retrosheet(date.year)
            rsheet.download_and_unzip(type='gamelog')
            
        #extract all the games on the given date
        with open(gamelogPath, "r") as f:
            list_of_games = [line.replace('"', '').split(',')[1:]
                                    for line in f if dateRFormat in line]

        # get the retrosheet ids from the games
        p = re.compile("[a-z]{5}[0-9]{3}")
        return [field for game in list_of_games
                    for field in game if re.match(p, field)]

    @classmethod
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
        
        Utilities.ensure_gamelog_files_exist(year)

        with open(Data.get_unzipped_gamelog_path(year), "r") as f:
            list_of_games = [line.replace('"', '').split(',')
                                    for line in f if date in line]
        homeTeamList = [game[6] for game in list_of_games 
                           if player.get_retrosheet_id() in game]
        return homeTeamList[0]
 
    @classmethod
    def did_start(self, date, player):
        """
        date: datetime.date(year, month, day) | a date in the year

        Returns: Boolean | True if player started a game on the given date, False otherwise
        """
        return player.get_retrosheet_id() in self.get_participants(date)

    @classmethod
    def did_get_hit(self, date, player):
        """
        date(year, month, day) Player -> Boolean

        date: a date in the year
        player: an MLB player

        Produces True if player got a hit on the given date, False otherwise 
            In the event that the player played in a double or triple header
            on the given date, returns True if and only if the player got a hit
            in the first game
        """
        team = self.find_home_team(date, player) # need home team's box score
        boxscore = Data.get_boxscore_file_path(date.year, team)
        lastName = player.get_last_name()
        firstName = player.get_first_name()

        # Ensure that boxscores are on the drive
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
                print "player: %s" % player
                print "Here's the line: %s" % (str(line))
                index = info[index + 1:].index(lastName)

            # Player's hit count is 5 off his last name. 
            return int(info[index+5]) > 0 

    @classmethod
    def num_at_bats(self, year, player):
        """
        int PlayerL -> int
        year: the year of interest
        PlayerL: A basic player-lahman object

        Produces the number of at bats that player had in year year
        """
        # get relevant columns from batting csv
        df = pd.read_csv(Data.get_lahman_path("batting"), 
                           usecols = ['playerID', 'yearID', 'AB'])
        # isolate info for player in year year
        df = df[df.playerID == player.get_lahman_id()][df.yearID == year]
        # calulate and return batting average
        return int(sum(df.AB))

    @classmethod
    def num_plate_appearances(self, year, player):
        """
        int PlayerL -> int
        year: the year of interest
        PlayerL: A basic player-lahman object

        Produces the number of plate appearances that player had in year year
        """
        # get relevant columns from batting csv
        df = pd.read_csv(Data.get_lahman_path("batting"), 
                usecols = ['playerID', 'yearID', 'AB', 'BB', 'HBP', 'SH', 'SF'])

        # isolate info for player in year year
        df = df[df.playerID == player.get_lahman_id()][df.yearID == year]

        # calculate plate appearances
        # PA = AB + BB + HBP + SH + SF
        PA = sum(df.AB) + sum(df.BB) + sum(df.HBP) + sum(df.SH) + sum(df.SF)
        return round(PA, 3)

    @classmethod
    def name_from_lahman_id(self, lahmanID):
        """
        string -> (string, string)
        lahmanID: the lahman ID of a MLB player

        Returns (firstName, lastName) for MLB player with id lahmanID
        """
        df = pd.read_csv(Data.get_lahman_path("master"), 
                            usecols=['playerID', 'nameLast', 'nameFirst'])
        df = df[df.playerID == lahmanID]
        return df.nameFirst.item(), df.nameLast.item()

    @classmethod
    def get_opening_day(self, year):
        """
        int -> date

        Produces the date of opening day in year year
        """
        Utilities.ensure_gamelog_files_exist(year)

        with open(Data.get_unzipped_gamelog_path(year), "r") as f:
            date_string = f.readline().split(',')[0]
        year = int(date_string[1:5])
        month = int(date_string[5:7])
        day = int(date_string[7:9])
        return date(year, month, day)

    @classmethod
    def get_closing_day(self, year):
       """
       int -> date

       Produces the date of closing day (of regular season) in year year
       """
       Utilities.ensure_gamelog_files_exist(year)
 
       # get last element in first--date--column of gamelog file
       df = pd.read_csv(Data.get_unzipped_gamelog_path(year), header=None)
       date_string = str(df[0].ravel()[-1])
       year = int(date_string[0:4])
       month = int(date_string[4:6])
       day = int(date_string[6:8])
       return date(year, month, day)