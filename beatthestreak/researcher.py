import datetime
import os
import re
import datetime

import pandas as pd
from datetime import date

from config import specialCasesD
from utilities import Utilities
from retrosheet import Retrosheet
from exception import FileContentException, BadDateException,\
     NotSuspendedGameException, SusGameDoesntFitCategoryException
from filepath import Filepath

class Researcher(object):
    """
    A MLB researcher that that look up facts about MLB events 
    (games, seasons, teams, etc)

    Note: functions with a Player or PlayerL instance as a parameter DO NOT 
    type check that parameter because importing from player.py would cause
    a cyclical import error

    Data:
       openAndCloseDays: a dictionary with key pair values:
          key: year as 4 digit int, value: (closingDay, openingDay) 
             where both values in value are of type datetime.date
          Has keys from 1963 to 2013, as this was written in 2014 and
          simulations before 1963 would have a different flavor since
          seasons were shorter
    """
    openAndCloseDays = {1963: (datetime.date(1963, 4, 8), datetime.date(1963, 9, 29)), 1964: (datetime.date(1964, 4, 13), datetime.date(1964, 10, 4)), 1965: (datetime.date(1965, 4, 12), datetime.date(1965, 10, 3)), 1966: (datetime.date(1966, 4, 11), datetime.date(1966, 10, 2)), 1967: (datetime.date(1967, 4, 10), datetime.date(1967, 10, 1)), 1968: (datetime.date(1968, 4, 10), datetime.date(1968, 9, 29)), 1969: (datetime.date(1969, 4, 7), datetime.date(1969, 10, 2)), 1970: (datetime.date(1970, 4, 6), datetime.date(1970, 10, 1)), 1971: (datetime.date(1971, 4, 5), datetime.date(1971, 9, 30)), 1972: (datetime.date(1972, 4, 15), datetime.date(1972, 10, 4)), 1973: (datetime.date(1973, 4, 5), datetime.date(1973, 10, 1)), 1974: (datetime.date(1974, 4, 4), datetime.date(1974, 10, 2)), 1975: (datetime.date(1975, 4, 7), datetime.date(1975, 9, 28)), 1976: (datetime.date(1976, 4, 8), datetime.date(1976, 10, 3)), 1977: (datetime.date(1977, 4, 6), datetime.date(1977, 10, 2)), 1978: (datetime.date(1978, 4, 5), datetime.date(1978, 10, 2)), 1979: (datetime.date(1979, 4, 4), datetime.date(1979, 9, 30)), 1980: (datetime.date(1980, 4, 9), datetime.date(1980, 10, 6)), 1981: (datetime.date(1981, 4, 8), datetime.date(1981, 10, 5)), 1982: (datetime.date(1982, 4, 5), datetime.date(1982, 10, 3)), 1983: (datetime.date(1983, 4, 4), datetime.date(1983, 10, 2)), 1984: (datetime.date(1984, 4, 2), datetime.date(1984, 9, 30)), 1985: (datetime.date(1985, 4, 8), datetime.date(1985, 10, 6)), 1986: (datetime.date(1986, 4, 7), datetime.date(1986, 10, 5)), 1987: (datetime.date(1987, 4, 6), datetime.date(1987, 10, 4)), 1988: (datetime.date(1988, 4, 4), datetime.date(1988, 10, 2)), 1989: (datetime.date(1989, 4, 3), datetime.date(1989, 10, 1)), 1990: (datetime.date(1990, 4, 9), datetime.date(1990, 10, 3)), 1991: (datetime.date(1991, 4, 8), datetime.date(1991, 10, 6)), 1992: (datetime.date(1992, 4, 6), datetime.date(1992, 10, 4)), 1993: (datetime.date(1993, 4, 5), datetime.date(1993, 10, 3)), 1994: (datetime.date(1994, 4, 3), datetime.date(1994, 8, 11)), 1995: (datetime.date(1995, 4, 25), datetime.date(1995, 10, 2)), 1996: (datetime.date(1996, 3, 31), datetime.date(1996, 9, 29)), 1997: (datetime.date(1997, 4, 1), datetime.date(1997, 9, 28)), 1998: (datetime.date(1998, 3, 31), datetime.date(1998, 9, 28)), 1999: (datetime.date(1999, 4, 4), datetime.date(1999, 10, 4)), 2000: (datetime.date(2000, 3, 29), datetime.date(2000, 10, 1)), 2001: (datetime.date(2001, 4, 1), datetime.date(2001, 10, 7)), 2002: (datetime.date(2002, 3, 31), datetime.date(2002, 9, 29)), 2003: (datetime.date(2003, 3, 30), datetime.date(2003, 9, 28)), 2004: (datetime.date(2004, 3, 30), datetime.date(2004, 10, 3)), 2005: (datetime.date(2005, 4, 3), datetime.date(2005, 10, 2)), 2006: (datetime.date(2006, 4, 2), datetime.date(2006, 10, 1)), 2007: (datetime.date(2007, 4, 1), datetime.date(2007, 10, 1)), 2008: (datetime.date(2008, 3, 25), datetime.date(2008, 9, 30)), 2009: (datetime.date(2009, 4, 5), datetime.date(2009, 10, 6)), 2010: (datetime.date(2010, 4, 4), datetime.date(2010, 10, 3)), 2011: (datetime.date(2011, 3, 31), datetime.date(2011, 9, 28)), 2012: (datetime.date(2012, 3, 28), datetime.date(2012, 10, 3)), 2013: (datetime.date(2013, 3, 31), datetime.date(2013, 9, 30))}
    
    # regular expression for matching retrosheet ids
    retroP = re.compile(r"""
        [a-z]{2}        # first two letters of last name
        [-a-z]{2}       # either 2 more letters of last name, or 1 more letter
                        # of the last name if player has a 3-digit last name
                        # (e.g lee) and a dash, or 2 dashes if player has 
                        # 2-digit last name (e.g hu)
        [a-z]{1}        # first letter of first name
        [0-9]{3}        # three numbers indicating role and sequence. See
                        # http://www.retrosheet.org/retroID.htm for more details
        """, re.VERBOSE)

    @classmethod
    # @profile
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
            self.__search_file(file, search, errorMessage=errorMessage)

            # find this player's line in the boxscore
            search = lastName + " " + firstName[0]
            errorMessage = "Player: {0} not in boxscore {1}.".format(player, 
                boxscore) + "Date: {0}".format(date)
            line = self.__search_file(file, search, errorMessage=errorMessage)

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
    def get_hit_info(self, date, player, sGD):
        """
        date Player dict -> bool|string None|String
           date: datetime.date | date of interest
           player: Player | Player of interest
           sGD: dict | A dictionary of suspended games in date.year, as defined
              in get_sus_games_dict

        Produces (hitResult, otherInfo) for player on given date. 
        Possible values of (hitResult, otherInfo):
            1) (True, None) # player got a hit on date date
            2) (False, None) # player did not get a hit on date date
            3) ('pass', 'Suspended, Invalid.'): # player played in a suspended, invalid game on date date
            4) (True, 'Suspended, Valid.'): # player got a hit in a suspended, valid game on date date
            5) (False, 'Suspended, Valid.'): # player did not get a hit in a suspended, valid game on date date

        Technically, this should also account for case 6 below, but because it is exceedingly rare,
        we do not account for it. This effectively makes our simulation slightly MORE conservative--i.e 
        more likely to reset a streak--than it should be, making us confident that at the worst, 
        playing for real should give us better results than our simulation
            6) ('pass', 'Screwy ABs'): # player played in a valid game on date date but all his at bats were 
                   either base on balls, hit batsman, defensive interference, defensive obstruction, 
                   or sacrifice bunt
        """
        # type check arguments (can't typecheck player because importing 
        # Player would cause circular imports)
        assert type(date) == datetime.date
        assert type(sGD) == dict

        if date in sGD.keys() and player.get_retrosheet_id() in sGD[date][1]:
            if sGD[date][0]: # Valid game
                return self.did_get_hit(date, player), specialCasesD['S']['V']
            else: # Invalid game
                return 'pass', specialCasesD['S']['I']
        else: # Normal game
            return self.did_get_hit(date, player), None

    @classmethod
    # @profile
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
            list_of_games = [
                line.replace('"', '').split(',') # get a list of entries in line
                for line in f                   # iterate through all lines in f
                if dateRFormat in line[0:10]] 
                   # by checking that the date is in the first 10 spots, we 
                   # gaurd against taking participants that played on the date
                   # a suspended game was completed. 

        # get the retrosheet ids from the games and return the list 
        return [field for game in list_of_games for field in game 
                    if re.match(self.retroP, field)]

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
    # @profile
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

        if year not in self.openAndCloseDays.keys():
            raise BadDateException("Researcher only handles seasons beetween" + \
                " {0} and {1}".format(1963, 2013))

        if not (date >= self.openAndCloseDays[year][0]) and \
            (date <= self.openAndCloseDays[year][1]):
            raise BadDateException("date {0} not in MLB {1} season".format(
                date, year))

    @classmethod
    def get_sus_games_dict(self, year):
        """
        int -> dict
        year: int | the year for which a simulation is being run

        Produces a dictionary with key, value pair types::
            datetime.date: (bool, TupleOfStrings)

        where the keys are dates on which a suspended game was played, 
              value[0] is True if the suspended game was valid, false otherwise,
              and value[1] is a tuple of all the retrosheetIDS for players
                 starting, managers managing, and umpires officiating in 
                 the suspended game
        """
        d = {}

        Utilities.ensure_gamelog_files_exist(year)

        with open(Filepath.get_retrosheet_file(folder='unzipped', 
            fileF= 'gamelog', year=year), "r") as f:
            for gameLine in f:
                if self.__is_game_suspended(gameLine):
                    gameLineTuple = gameLine.replace('"', '').split(',')
                    susDay = date(int(gameLine[1:5]), int(gameLine[5:7]), 
                        int(gameLine[7:9]))
                    d[susDay] = (self.__is_suspended_game_valid(gameLine), 
                        tuple([item for item in gameLineTuple if 
                            re.match(self.retroP, item)]))
        return d

    @classmethod
    def __is_suspended_game_valid(self, game):
        """
        str -> bool
        game: str | a single line from a retrosheet gamelog, which
            provides information about a MLB game

        Returns true if suspended game is "valid" and returns false 
        if if not. Raises error if game is not suspended or none of the
        below categories are met
           Motivation for "validity"
               If a suspended game is valid, it is eligible to either lenghthen
               or end a bot's streak as per beatthestreak official rules. 
               If a suspended game is invalid, bot's get a pass for date date, 
               leaving their streak where it is. 
           Definition for "validity"
               A game is valid if:
                   1) >= 5 innings were completed prior to suspension
                   2) The game was suspended in the 5th inning and
                      at the time of suspension, the visiting team trailed
                        and >= 3 outs were completed in the 5th inning
                   3) The game was suspended in the 5th inning and at the time
                      of suspension, the game was tied and >= 3 outs were
                      completed in the 5th inning
                A game is invalid in the complementary cases:
                   1) <= 4 innings were completed prior to suspension
                   2) The game was suspended in the 5th inning and (at the time
                      of suspension, the visiting team trailed and <= 2 outs
                      were completed in the 5th inning) or (at the time of
                      suspension, the home team trailed and <= 5 outs were 
                      completed in the 5th inning)
                   3) The game was suspended in the 5th inning and at the time 
                      of suspension, the game was tied and <= 2 outs were 
                      completed in the 5th inning. 
        """
        assert type(game) == str
        
        # Make sure its actually a suspended game
        if not self.__is_game_suspended(game):
            raise NotSuspendedGameException("The below game is not" + \
                "a suspended game!\n{0}".format(game))

        # sus Data is 'dateOfCompletion (dOC), parkOfCompletionID (pCID)
        # vistorScoreAtTimeOfSuspension (vSS), homeScoreAtTimeOfSUspension (hSS), 
        # lengthOfGameatTimeOfSUspension (numOutsSus)'
        susData = game.split('"')[17]
        susDataTuple = susData.split(',')
        vSS = int(susDataTuple[2])
        hSS = int(susDataTuple[3])
        numOutsSus = int(susDataTuple[4])
        
        # Check for valid condition 1 and invalid condition 1
        if numOutsSus >= 30: # >= 5 innings played
            return True
        if numOutsSus <= 24: # <= 4 innings played
            return False

        # Check for valid conditions 2 and 3 and invalid conditions 2 and 3
        if numOutsSus in (25, 26): # <= two innings played in 5th
            return False
        if numOutsSus in (27, 28, 29):
            if hSS < vSS: # If the home team was trailing
                return False
            else:         # if the visitors trailed or the game was tied
                return True

        # If the game somehow slipped through every condition, raise exception
        raise SusGameDoesntFitCategoryException("The suspended game does not" +\
            "fit any of the MLB Beatthestreak categories\n{0}".format(game)) # pragma: no cover (Can't think of a test case)

    @classmethod
    def __is_game_suspended(self, game):
        """
        str -> bool
        game: str | a single line from a retrosheet gamelog, which
            provides information about a MLB game

        Returns true if game was suspended and false otherwise
        """
        assert type(game) == str
        # column 14 contains a yyyymmdd date string if the game was suspended
        # and completed on the date in column 14, and is empty otherwise
        item14 = game.replace('"','').split(',')[13]
        # p regex matches a yyyymmdd string
        p = re.compile(r"""
            [1-2]{1}[0-9]{3}       # yyyy
            [0-1]{1}[1-9]{1}       # mm
            [0-3]{1}[0-9]{1}       # dd
            """,re.VERBOSE)
        return re.match(p, item14)
           
    @classmethod 
    def __search_file(self, fileF, search, errorMessage='Search File Error'):
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