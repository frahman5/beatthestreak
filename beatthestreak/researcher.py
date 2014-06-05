import datetime
import os
import re
import pandas as pd

from datetime import date

from utilities import Utilities
from retrosheet import Retrosheet
from exception import FileContentException, BadDateException
from filepath import Filepath

class Researcher(object):
    """
    A MLB researcher. He is a container that holds functions 
    that look up facts about MLB events (games, seasons, teams, etc)

    Note: functions with a Player or PlayerL instance as a parameter DO NOT 
    type check that parameter because importing from player.py would cause
    a cyclical import error
    """
    @classmethod
    def did_get_hit(self, date, player):
        """
        date Player -> bool
        date: date | a date in the year
        player: player | MLB player of interest

        Returns True if player got a hit on the given date, False otherwise 
            In the event that the player played in a double or triple header
            on the given date, returns True if and only if the player got a hit
            in the first game
        """
        assert type(date) == datetime.date
        self.check_date(date, date.year)

        # Ensure that boxscores are on the drive
        team = self.find_home_team(date, player) 
        Utilities.ensure_boxscore_files_exist(date.year, team)

        # Get home team's box score and player's first and last names
        boxscore = Filepath.get_retrosheet_file(folder='unzipped', 
            fileF='boxscore', year=date.year, team=team)
        lastName = player.get_last_name()
        firstName = player.get_first_name()
        
        with open(boxscore, "r") as file: 
            # find this date's game in the boxscore
            search = str(date.month) + "/" + str(date.day) + "/" + str(date.year)
            errorMessage = "Date: {0} not in boxscore {1}.".format(date, 
                boxscore) + "Player: {0}".format(player)
            self._search_file(file, search, errorMessage=errorMessage)

            # find this player's line in the boxscore
            search = lastName + " " + firstName[0]
            errorMessage = "Player: {0} not in boxscore {1}.".format(player, 
                boxscore) + "Date: {0}".format(date)
            line = self._search_file(file, search, errorMessage=errorMessage)

            # see if he had a hit or not
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
    def find_home_team(self, date, player):
        """
        date Player -> String
        date: date | a date in the year during the MLB season
        Player: Player | a player participating in a game on the given date

        Produces a three digit abbreviation for the home team that played
            a game involving given player on given date
        """
        assert type(date) == datetime.date
        self.check_date(date, date.year)

        year = date.year
        date = Utilities.convert_date(date)
        Utilities.ensure_gamelog_files_exist(year)
        
        # get list of games played on this date
        with open(Filepath.get_retrosheet_file(folder='unzipped', 
            fileF='gamelog', year=year), "r") as f:
            list_of_games = [line.replace('"', '').split(',') for line in f 
                             if date in line]

        # Find the game that player played in, and get the home team
        # we check if date in game[0] because a game may have ended up in 
        # in the list from some incomplete game thats being completed on a later
        # date. See Lance Berkman, 2009-July-9th
        homeTeamList = [game[6] for game in list_of_games  
                        if player.get_retrosheet_id() in game 
                        and date in game[0]]
        return homeTeamList[0]

    @classmethod
    def did_start(self, date, player):
        """
        date Player -> bool
        date: date | a date in the year
        player: Player | the player of interest

        Returns: True if player started a game on the given date, False otherwise
        """
        assert type(date) == datetime.date
        self.check_date(date, date.year)

        return player.get_retrosheet_id() in self.get_participants(date)

    @classmethod
    def num_at_bats(self, year, player):
        """
        int PlayerL -> int
        year: int | the year of interest
        PlayerL: PlayerL | A basic player-lahman object of interest

        Produces the number of at bats that player had in year year
        """
        assert type(year) == int

        # get relevant columns from batting csv
        df = pd.read_csv(Filepath.get_lahman_file("batting"), 
                           usecols = ['playerID', 'yearID', 'AB'])
        # isolate info for player in year year
        df = df[df.playerID == player.get_lahman_id()][df.yearID == year]
        # calulate and return batting average
        return int(sum(df.AB))

    @classmethod
    def num_plate_appearances(self, year, player):
        """
        int PlayerL -> int
        year: int | the year of interest
        PlayerL: int| A basic player-lahman object of interest

        Returns the number of plate appearances that player had in year year
        """
        assert type(year) == int

        # get relevant columns from batting csv
        df = pd.read_csv(Filepath.get_lahman_file("batting"), 
                usecols = ['playerID', 'yearID', 'AB', 'BB', 'HBP', 'SH', 'SF'])

        # isolate info for player in year year
        df = df[df.playerID == player.get_lahman_id()][df.yearID == year]

        # calculate and return plate appearances
        # PA = AB + BB + HBP + SH + SF
        PA = sum(df.AB) + sum(df.BB) + sum(df.HBP) + sum(df.SH) + sum(df.SF)
        return PA

    @classmethod
    def get_participants(self, date):
        """
        date -> ListOfStrings   
        date: date | a date of the year

        Produces a list of retrosheet ids corresponding to players starting, 
        umps officiating, and managers managing on the given day
        """
        assert type(date) == datetime.date
        self.check_date(date, date.year)
        dateRFormat = Utilities.convert_date(date) # date in yyyymmdd format

        Utilities.ensure_gamelog_files_exist(date.year)

        # extract all the games on the given date
        gamelogPath = Filepath.get_retrosheet_file(folder='unzipped', 
            fileF='gamelog', year=date.year)
        with open(gamelogPath, "r") as f:
            list_of_games = [line.replace('"', '').split(',')[1:]
                                    for line in f if dateRFormat in line]

        # get the retrosheet ids from the games and return the list 
        p = re.compile("[a-z]{5}[0-9]{3}")
        return [field for game in list_of_games for field in game 
                    if re.match(p, field)]

    @classmethod
    def get_opening_day(self, year):
        """
        int -> date

        Returns the date of opening day in year year
        """
        assert type(year) == int 

        Utilities.ensure_gamelog_files_exist(year)
 
        # get first item in gamelog for year year, which is opening day
        with open(Filepath.get_retrosheet_file(folder='unzipped', 
            fileF='gamelog', year=year), "r") as f:
            date_string = f.readline().split(',')[0]

        # format and return the date
        year = int(date_string[1:5])
        month = int(date_string[5:7])
        day = int(date_string[7:9])
        return date(year, month, day)

    @classmethod
    def get_closing_day(self, year):
       """
       int -> date

       Returns the date of closing day (of regular season) in year year
       """
       assert type(year) == int

       Utilities.ensure_gamelog_files_exist(year)
 
       # get last element in first column (the date column) of gamelog file
       df = pd.read_csv(Filepath.get_retrosheet_file(folder='unzipped', 
          fileF='gamelog', year=year), header=None)
       date_string = str(df[0].ravel()[-1])

       # format and return the date
       year = int(date_string[0:4])
       month = int(date_string[4:6])
       day = int(date_string[6:8])
       return date(year, month, day)

    @classmethod
    def name_from_lahman_id(self, lahmanID):
        """
        string -> (string, string)
        lahmanID: string | the lahman ID of a MLB player

        Returns (firstName, lastName) for MLB player with id lahmanID
        """
        assert type(lahmanID) == str

        # get relevant files from master csf
        df = pd.read_csv(Filepath.get_lahman_file("master"), 
                            usecols=['playerID', 'nameLast', 'nameFirst'])
        # isolate rows for player with lahmanID
        df = df[df.playerID == lahmanID]
        # return his first and last names
        return df.nameFirst.item(), df.nameLast.item()

    @classmethod
    def check_date(self, date, year):
        """
        date int -> bool
        date: date | a date in the year
        year: int | a year

        Produces true if date was one of active days of the MLB regular season
        in year year
        """
        assert type(date) == datetime.date
        assert type(year) == int

        if not ((date >= self.get_opening_day(year)) and \
            (date <= self.get_closing_day(year))):
            raise BadDateException("date {0} not in MLB {1} season".format(
                date, year))
            
    @classmethod
    def _search_file(self, fileF, search, errorMessage='Search File Error'):
        """
        fileF string string -> string
        file: file| a file object to be searched
        search: string | a string to search for in the file
        errorMessage: stirng | the error Message to display if 
            an exception is raised


        Searches the file for the string. If found, returns the line in which
        the string was found. If not found, raises fileContentException
        """
        assert type(fileF) == file
        assert type(search) == str
        assert type(errorMessage) == str

        line = " "
        while search not in line: 
            start = fileF.tell()
            line = fileF.readline()
            end = fileF.tell()
            # if we keep scrolling and the file position doesn't change, 
            # the search item was not in the file
            if start == end: 
                raise FileContentException(errorMessage)
        return line