from simulation import Simulation
import pandas as pd

from data import Data
from player import PlayerL
from researcher import Researcher
from exception import DifficultYearException

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
    def __init__(self, simYear, batAveYear, N, P):
        Simulation.__init__(self, simYear)
        self.num_robots = N
        self.num_players = P
        self.min_bat_ave = self.__calc_min_bat_ave(P, batAveYear)

    def __calc_min_bat_ave(self, P, year):
        """
        int int -> float
        P: an int representing the number of top players
           participating in this simulation, where top
           refers to best batting averages
        year: year in which to consider batting averages

        Produces the highest 3 digit float f such that
        for all P players {p1, p2, .., pP}, 
        pi_bat_ave >= f.
        """ 
        # minReqABs = 425 # minimum required at bats

        # Since 1962 the season has been 162 games and 3.1 PAs per game, or 502
        # pers season has been the min requirement for batting title contention.
        # This figure is altered for the strikeYears and years before 1962.
        strikeYearsSince1962 = (1972, 1981, 1994, 1995)
        if (year > 1962) and (year not in strikeYearsSince1962):
            minPA = 502
        else:
            raise DifficultYearException("The years 1972, 1981, 1994, 1995 " + \
                "had strikes, and the years before 1962 didn't have 162 games." + \
                " Please simulate in another year") 
        battingAverages = [0 for i in range(P)]
        players = [('', 0) for i in range(P)] # debugging

        # read in playerID and yearID columns from batting.csv, 
        # then splice out all rows not corresponding to year year
        df = pd.read_csv(Data.get_lahman_path("Batting"), 
                           usecols=['playerID', 'yearID', 'AB'])
        df = df[df.yearID == year]

        # get series of unique playerIDs
        uniqueIDs = pd.Series(df.playerID.values.ravel()).unique()

        # calculate all batting averages, and maintain sorted list
        # of top P batting averages
        i = 0
        for lahmanID in uniqueIDs:
            i += 1
            if i % 200 == 0:
                print i
            player = PlayerL(lahmanID, year)
            bat_ave = player.get_bat_ave()
            if  bat_ave > battingAverages[0]:
                if Researcher.num_plate_appearances(year, player) >= minPA:
                    battingAverages[0] = bat_ave
                    players[0] = (Researcher.name_from_lahman_id(lahmanID), bat_ave)
                    battingAverages.sort()
                    players.sort(key=lambda duple: duple[1])
        players.reverse()
        for duple in players:
            print "%s: %f" % (duple[0], duple[1])
        return round(battingAverages[0], 3)

    def get_min_bat_ave(self):
        return self.min_bat_ave

    def set_n(self, N):
        self.num_robots = N

    def get_n(self):
        return self.num_robots

    def set_p(self, P):
        self.num_players = P

    def get_p(self):
        return self.num_players