##### BEFORE SIMULATING, need to adjust this to be able to handle any year. 
##### Currently only works for 2012
import os

from datetime import date
from data import Data as data
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
        teams: ListOfStrings | team's the player played for in the relevant season
            -> Simulation should pass in correct season
    """
    
    def __init__(self, index, first_n, last_n, bat_ave, year):
        self.index = index
        self.first_name = first_n
        self.last_name = last_n
        self.id = self.set_retrosheet_id()
        self.bat_ave = bat_ave
        self.teams = self.set_teams(year)
    
    def did_start(self, date):
        """
        date: datetime.date(year, month, day) | a date in the year

        Returns: Boolean | True if player started a game on the given date, False otherwise
        """
        researcher = Researcher()
        return self.get_retrosheet_id() in researcher.get_participants(date)

    def find_home_team(self, date):
        """
        date: datetime.date(year, month day) | a date in the year

        Returns: String | three digit abbreviation for home team that played
            a game including given player on given date
        """
        date = Utilities.convert_date(date)
        with open(data.rootDir + data.gl2012Suffix, "r") as f:
            list_of_games = [line.replace('"', '').split(',')
                                    for line in f if date in line]
        homeTeamList = [game[6] for game in list_of_games if self.id in game]
        return homeTeamList[0]

    def did_get_hit(self, date):
        """
        date: date(year, month, day) | a date in the year

        Returns: Boolean | True if player got a hit on the given date, False otherwise 
            Assumes necessary retrosheet files have been extracted (done by simulation)
        """
        os.chdir(data.rootDir + data.defaultDestUnzippedSuffix + \
                     "/events" + str(date.year))
        team = self.find_home_team(date) # must use the box score from home team
        with open(str(date.year) + team + "B.txt", "r") as file: 
            line = ""

            # find this date's game's boxscore
            search = str(date.month) + "/" + str(date.day) + "/" + str(date.year)
            while search not in line: line = file.readline()

            # find this player's line in the boxscore
            search = self.last_name + " " + self.first_name[0]
            while search not in line: line = file.readline()

            #find the index of this player's last name in the line
            info = line.split()
            index = info.index(self.last_name)
            if info[index + 1] != self.first_name[0] + ",":
                print "We had two lined up players with same last name!" 
                print "Here's the line: %s" % (str(line))
                index = info[index + 1:].index(self.last_name)

            # Player's hit count is 5 off his last name. 
            return int(info[index+5]) > 0

        #Make it work for a player who got traded. Test MUCH more robustly. 

    def set_retrosheet_id(self):
        """
        name: string | name of player

        Returns: string | retrosheet id of player
            If player name has multiple ids, prompts user to choose one
        """
        name = self.last_name + "," + self.first_name
        
        # Get list of possible ids
        with open(data.rootDir + data.rIdSuffix, "r") as f:
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

    def set_teams(self, year):
        eventsDir = data.rootDir + data.defaultDestUnzippedSuffix + \
                     "/events" + str(year)

        # check to make sure we have the necessary event files
        if not os.path.isdir(eventsDir):
            retrosheet = Retrosheet(year)
            retrosheet.download()
            retrosheet.unzip()
        
        # get the teams from the event files
        os.chdir(data.rootDir + data.defaultDestUnzippedSuffix + \
                     "/events" + str(year))
        teams = [file[0:3] for file in os.listdir(os.getcwd()) if 
                     file.endswith("ROS") and self.id in open(file).read()]
        return teams

    def get_teams(self):
        return self.teams
    
    def get_index(self):
        return self.index
    
    def get_name(self):
        return self.first_name + " " + self.last_name
    
    def get_bat_ave(self):
        return self.bat_ave
