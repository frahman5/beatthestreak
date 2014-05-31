from simulation import Simulation
import pandas as pd

from data import Data
from datetime import date, timedelta
from player import PlayerL, Player
from researcher import Researcher
from exception import DifficultYearException
from bot import Bot

class NPSimulation(Simulation):
    """
    A BTS simulation using the NP strategy. 

    NP Strategy denotes a number N of robots and a number P 
    of MLB players. Each robot is a MLB BTS account and hence its own
    individual participant in the contest. The P players represent the
    P players with the highest batting averages for the time in consideration.
    Top batting averages may be calculated with respect to the season in which
    the simulation is being run, prior seasons, or player careers. 
        -> NOTE: currently career batting ave calculations are unsupported

    
    NOTE: DESCRIBE STRATEGY IN DETAIL HERE
    """
    def __init__(self, simYear, batAveYear, N, P, startDate='default'):
        Simulation.__init__(self, simYear, startDate)
        self.simYear = self.check_year(simYear)
        self.batAveYear = self.check_year(batAveYear)
        self.numBots = N
        self.numPlayers = P
        self.minBatAve = 0 # set later, upon setup of sim
        self.players = [] # set later, upon setup of sim
        self.bots = []
        if startDate == 'default':
            self.currentDate = Researcher.get_opening_day(simYear)
        else:
            assert type(startDate) == date
            self.currentDate = startDate
        self.isSetup = False

    def setup(self):
        if self.isSetup: 
            return
        Simulation.setup(self) # download and parse retrosheet data
        self.bots = self.__create_bots() # create N bots
        self.players = self.__calc__players(self.batAveYear) # get P top players
        self.minBatAve = self.__set_min_bat_ave() # store resultant min bat ave
        self.isSetup = True

    def sim_next_day(self):
        """
        None -> None

        Simulates the next day
        """
        print "at start of sim"
        # import pdb
        # pdb.set_trace()
        # which players were active?
        activePlayers = [player for player in self.players if \
             Researcher.did_start(self.currentDate, player)]
        print "at line 63 in sim"
        # assign players to bots
        mod_factor = len(activePlayers)
        for i, bot in enumerate(self.bots):
            player = activePlayers[i % mod_factor]
            print "current player: "
            print player
            bot.assign_player(player, Researcher.did_get_hit(self.currentDate, player))
        print "at line 69 in sim"
        # update the date
        self.incr_date()
        print "finished sim"

        
    def __calc__players(self, year):
        """
        None -> ListOfTuples(player, player.bat_ave)
        Calculates the top P players with respect to batting average
        in season self.batBatAveYear
        """
        minPA = 502 # minimum plate appearances to qualify for calculation
        players = [("", 0) for i in range(self.numPlayers)]

        #get series of unique playerIDs corresponding to given year
        df = pd.read_csv(Data.get_lahman_path("Batting"), 
                           usecols=['playerID', 'yearID', 'AB'])
        df = df[df.yearID == year]
        uniqueIDs = pd.Series(df.playerID.values.ravel()).unique()

        # Calculate top P players/batting averages
        for index, lahmanID in enumerate(uniqueIDs):
            # if type(players[0][0]) == PlayerL:
            #     break
            if index % 200 == 0: print index # progress tracker
            player = PlayerL(lahmanID, year)
            bat_ave = player.get_bat_ave()
            if  bat_ave > players[0][1]:
                if Researcher.num_plate_appearances(year, player) >= minPA:
                    players[0] = (player, bat_ave)
                    players.sort(key=lambda duple: duple[1])
        players.reverse() # list is now from highest to lowest

        # turn players into full blown players, and index accordingly. 
        for index, tuple in enumerate(players):
            players[index] = Player(index, playerL=tuple[0])
        return players

    def check_year(self, year):
        """
        int -> None|int
        Produces an exception if year is before 1962 or a strike year (1972, 
            1982, 1994, 1995) since 1962. Returns the given year otherwise.
        """
        # Since 1962 the season has been 162 games and 3.1 PAs per game, or 502
        # per season has been the min requirement for batting title contention.
        # This figure is altered for the strikeYears and years before 1962.
        if (year <= 1962) or (year in (1972, 1981, 1994, 1995)):
            raise DifficultYearException("The years 1972, 1981, 1994, 1995 " + \
                "had strikes, and the years before 1962 didn't have 162 games." + \
                " Please simulate in another year") 
        else:
            return year

    def get_players(self):
        return self.players

    def __set_min_bat_ave(self):
        """
        Helper function for setup. Feeds off of __calc__players

        Produces the highest 3 digit float f such that for all P players 
        {p1, p2, .., pP}, pi_bat_ave >= f.
        """ 
        return self.players[-1].get_bat_ave()

    def get_min_bat_ave(self):
        return self.minBatAve

    def __create_bots(self):
        return [Bot(i) for i in range(self.numBots)]

    def get_bots(self):
        return self.bots

    def set_n(self, N):
        self.numRobots = N

    def get_n(self):
        return self.numRobots

    def set_p(self, P):
        self.numPlayers = P

    def get_p(self):
        return self.num_players

    def set_date(self, date):
        self.currentDate = date
    
    def get_date(self):
        return self.currentDate

    def incr_date(self, num_days=1):
        """
        int -> None
        increment self.currentDate by num_days
        """
        self.currentDate += timedelta(days=num_days)
    
    def get_sim_year(self):
        return self.simYear

    def get_bat_year(self):
        return self.batAveYear