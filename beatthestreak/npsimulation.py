import sys
import os

from pandas import DataFrame, Series, ExcelWriter
from datetime import date, timedelta
from progressbar import ProgressBar
from progressbar.widgets import Timer, Percentage

from filepath import Filepath
from simulation import Simulation
from player import PlayerL, Player
from researcher import Researcher
from exception import DifficultYearException, InvalidResultsMethodException
from bot import Bot
from npreporter import NPReporter

class NPSimulation(Simulation):
    """
    A BTS simulation using the NP strategy. 

    NP Strategy denotes a number N of robots and a number P of MLB players. 

    Strategy: The Simulation initalizes N robots (accounts) and calculates the P
    "best" players ordered by highest seasonal batting average. Each
    day, it checks which of the P players are playing in a game and then assigns
    the active ones to the bots in order from highest batting average to lowest, 
    repeating the list of P players as many times as needed to assign a player
    to every bot. 

    Currently only handles regular season
    """
    def __init__(self, simYear, batAveYear, N, P, startDate='default'):
        Simulation.__init__(self, simYear, startDate)
        self.batAveYear = self._check_year(batAveYear)
        self.numBots = N
        self.numPlayers = P

        self.minBatAve = 0 # set upon setup
        self.players = [] # set upon setup
        self.bots = [] # set upon setup
        self.isSetup = False

        self.outputMethods = ('stdout', 'excel')

    def setup(self):
        """
        Downloads necessary retrosheet data, initalizes bots, players, minBatAve
        """
        if self.isSetup: 
            return

        Simulation.setup(self) # download and parse retrosheet data
        self.bots = self._create_bots() # create N bots
        self.players = self.__calc__players(self.batAveYear) # create top P players
        self.minBatAve = self.__set_min_bat_ave() # store resultant min bat ave
        self.isSetup = True

    def sim_next_day(self):
        """
        None -> None

        Simulates the next day
        """
        today = self.get_date()

        if self.get_date().day % 10 == 0: # progress indicator
            print "Simming day: {0}".format(today) 

        # Retrieve list of players playing today
        activePlayers = [player for player in self.players if \
             Researcher.did_start(today, player)]

        # assign players to bots
        mod_factor = len(activePlayers)
        if mod_factor == 0: # no activePlayers today
            self.incr_date()
            return 
        for i, bot in enumerate(self.bots):
            player = activePlayers[i % mod_factor]
            bot.update_history(player, 
                Researcher.did_get_hit(today, player), today)

        # update the date
        self.incr_date()
    
    def simulate(self, numDays='max', anotherSim=False, resultsMethod='excel'):
        """
        int|string  bool string-> None
        numDays: int|string | 'max' if simulation should run to closing day, 
            or an integer if simulation should run for a certain window of days
        anotherSim: bool | indicates whether or not another simulation will be 
            done using this object
        resultsMethod: TupleOfInts | Indicates preferred method of output
            -> must be in self.outputMethods


        Simulates numDays number of days in self.simYear starting on 
        self.get_date(). Reports back the number of bots who achieved streaks
        of greater than 57, as well as their respective streak lengths. Reports
        back a variable number of top bots, inluding their player histories. 
        """
        assert (type(numDays) == str) or (type(numDays) == int)
        assert type(anotherSim) == True
        assert type(resultsMethod) == str
        assert resultsMethod in self.outputMethods

        # initalize relevant date variables and setup the simulation
        startDate = self.currentDate
        lastDate = Researcher.get_closing_day(self.simYear)
        Reporter = NPReporter(self)
        self.setup()
 
        # simulate days until lastDate reached or elapsedDays equals numDays
        elapsedDays = 0
        while True:
            if (numDays=='max') and (self.currentDate > lastDate):
                Reporter.report_results(method=resultsMethod)
                break
            if (type(numDays) == int) and elapsedDays >= numDays:
                Reporter.report_results(method=resultsMethod)
                break
            self.sim_next_day()
            elapsedDays += 1
        
        # close up shop
        if anotherSim:
            self.set_setup(value=False)
        else:
            self.close() 
        
        # alert user that simulation is over
        print "Simulation simYear: {1}, batAveYear: {2} ".format(
            self.get_sim_year(), self.get_bat_year()) + \
            "N: {1}, P: {2} over!".format(self.get_n(), self.get_p())

    def mass_simulate(self, simYearRange, simMinBatRange, NRange, PRange):
        """
        tupleOfInts tupleOfInts tupleOfInts tupleOfInts -> None
        simYearRange: the years (inclusive) over which to run simulation
        simMinBatRange: the number of years (inclusive) over which to vary 
            simYear - batAveYear
        NRange: the integers (inclusive) over which to vary the number of bots
        PRange: the integers (inclusive) over which to vary top player calculations

        For each year in simYearRange, for each batAveYear that results from
        subtracting a number in simMinBatRange from simYear, for each N in NRange, 
        take a P from P Range and run simulate. Report aggregate results in an 
        excel file.

        e.g: sim.many_simulate((2010,2010),(0,1), (1,2), (1,2)) runs a simulation
        for each 4-tuple (simYear, batAveYear, N, P) with numDays='max' below. 
        Reports results in an excel file
            1) (2010, 2010, 1, 1)
            2) (2010, 2010, 1, 2)
            3) (2010, 2010, 2, 1)
            4) (2010, 2010, 2, 2)
            5) (2010, 2009, 1, 1)
            6) (2010, 2009, 1, 2)
            7) (2010, 2009, 2, 1)
            8) (2010, 2010, 2, 2)
        """
        for param in (simYearRange, simMinBatRange, NRange, PRange):
            for item1, item2 in param:
                assert type(item1) == type(item2) == int

        # lists hold data that will later be written to .xlsxfile
        simYearL, batAveYearL, NL, PL , minBatAveL = [], [], [], [], []
        numSuccessL, percentSuccessL, numFailL, percentFailL = [], [], [], []

        # initialize a progressbar for the simulation
        maxval = len(range(simYearRange[0], simYearRange[1] + 1)) * \
                 len(range(simMinBatRange[0], simMinBatRange[1] + 1)) * \
                 len(range(NRange[0], NRange[1] + 1)) * \
                 len(range(PRange[0], PRange[1] + 1))
        widgets = ['Running simulations with simYear:({0}, {1}), '.format(
            simYearRange[0], simYearRange[1]) + 'simMinBatRange({0}, {1}'.format(
                simMinBatRange[0], simMinBatRange[1]), + ' N:{0} , P: {1}'.format(
                self.get_n(), self.get_p()), Timer(), ' ', Percentage()]
        pbar = ProgressBar(maxval=maxval, widgets=widgets).start()

        # run all the simulations, saving individual simulation results to file
        i = 0
        for simYear in simYearRange:
            for batAveYear in self.__bat_years_ms(simYear, simMinBatRange):
                for N in NRange:
                    for P in PRange:
                        # set sim parameters and simulate
                        self.set_sim_year(simYear)
                        self.set_bat_year(batAveYear)
                        self.set_n(N)
                        self.set_p(P)
                        self.simulate(anotherSim=True)

                        # record sim metadata and results for later reporting
                        simYearL.append(self.get_sim_year())
                        batAveYearL.Append(self.get_bat_year())
                        NL.append(self.get_n())
                        PL.append(self.get_p())
                        minBatAveL.append(self.get_min_bat_ave())
                        numS, percS, numF, percF = self.calc_s_and_f()
                        numSuccessL.append(numS)
                        percentSuccessL.append(percS)
                        numFailL.append(numF)
                        percentFailL.append(percF)

                        # update progress bar
                        i += 1
                        pbar.update(i)
        pbar.finish() # kill the progress bar after the simulation ends

        # report aggregate results
        print "Reporting aggregate results to file"
        Reporter = NPReporter(self)
        Reporter.report_mass_results_excel(
            simYearL=simYearL, batAveYearL=batAveYearL, NL=NL, PL=PL, 
            minBatAveL=minBatAveL, numSuccessL=numSuccessL, 
            percentSuccessL=percentSuccessL, numFailL=numFailL, 
            percentFailL=percentFailL, simYearRange=simYearRange, 
            simMinBatRange=simMinBatRange, NRange=NRange, PRange=PRange)

        # close up shop
        self.close()

    def get_players(self):
        return self.players

    def get_min_bat_ave(self):
        return self.minBatAve

    def _create_bots(self):
        return [Bot(i) for i in range(self.numBots)]

    def get_bots(self):
        return self.bots

    def set_n(self, N):
        self.numBots = N

    def get_n(self):
        return self.numBots

    def set_p(self, P):
        self.numPlayers = P

    def get_p(self):
        return self.numPlayers

    def incr_date(self, num_days=1):
        """
        int -> None
        increment self.currentDate by num_days
        """
        self.currentDate += timedelta(days=num_days)

    def set_bat_year(self, year):
        self.batAveYear = year

    def get_bat_year(self):
        return self.batAveYear

    def set_setup(self, value=False):
        self.isSetup = value

    def get_setup(self):
        return self.isSetup

    def __bat_years_ms(self, simYear, simMinBatRange):
        """
        int tupleOfInts -> generatorOfInts
        simYear: int | year of simulation 
        simMinBatRange:  (minYearsToSubtractFromSimYear,
                          maxYearsToSubtractFromSimYear)

        Returns the batting average years for a mass simulation in year simYear
        with values for simYear-batAveYear between simMinBatRange[0] and
        simMinBatRange[1]
        """
        self._check_year(simYear)
        assert (type(simMinBatRange) == tuple)
        for item in simMinBatRange:
            assert type(item) == int

        return (simYear - difference for difference 
            in range(simMinBatRange[0], simMinBatRange[1] + 1))
  
    def __calc__players(self, year):
        """
        int -> ListOfTuples(player, player.bat_ave)

        Calculates the top P players with respect to batting average
        in season year
        """
        self._check_year(year)

        # set initial variables
        minPA = 502 # minimum plate appearances to qualify for calculation
        players = []

        # check if the file with batting Averages for year year has
        # already been constructed, if not construct it
        if not os.path.isfile(Filepath.get_retrosheet_file(folder='persistent', 
            fileF='batAve', year=year)):
            self.__construct_bat_ave_csv(year)

        # Initialize a progressbar
        widgets = \
            ['    Calculating the top {0} players in year {1} from file '.format(
            self.get_p(), self.get_bat_year()), Timer(), ' ', Percentage()]
        pbar = ProgressBar(maxval=self.get_p(), widgets=widgets).start()

        # Construct a list of the top P players
        df = DataFrame.from_csv(Filepath.get_retrosheet_file(folder='persistent', 
            fileF='batAve', year=year))
        lenPlayers, P = 0, self.get_p()
        for lahmanID, batAve, PA in df.itertuples():
            if lenPlayers == P: # we've got all the players
                break
            if PA >= minPA: # make sure the player has enough plate appearances
                players.append(Player(lenPlayers, playerL=PlayerL(lahmanID, year)))
                lenPlayers += 1
                pbar.update(lenPlayers)
        pbar.finish() # kill the progressbar

        return players

    def __construct_bat_ave_csv(self, year):
        """
        int -> None
        year: int | the year for which the csv file should be constructed

        Produces a csv with lahmanIDs, corresponding batting averages, 
        and plate appearances in year year, sorted by batting average column. 
        Saves it to file. (Helper function for _calc_players)
        """
        self._check_year(year)

        # Set initial variables
        batAveCol = 'batAve' + str(year) + 'Sorted'
        
        # get series of unique playerIDs corresponding to given year
        df = read_csv(Filepath.get_lahman_file("Batting"), 
                           usecols=['playerID', 'yearID', 'AB'])
        df = df[df.yearID == year]
        uniqueIDArray = Series(df.playerID.values.ravel()).unique()
             # uniqueIDArray is of type ndarray

        # Initalize progressbar
        widgets = ['     Creating batting average csv for year %s ' % year, 
            Timer(), ' ', Percentage()]
        pbar = ProgressBar(maxval=len(uniqueIDArray), widgets=widgets).start()

        # calculate batting averages and plate appearances
        batAveList, plateAppearList = [], []
        for index, lahmanID in enumerate(uniqueIDArray):
            player = PlayerL(lahmanID, year)
            batAveList.append(player.get_bat_ave())
            plateAppearList.append(Researcher.num_plate_appearances(year, player))
            pbar.update(index)
        pbar.finish() # kill the proress bar

        # Write the data to csv
        batAveS = Series(batAveList, name=batAveCol)
        plateAppearS = Series(plateAppearList, name='PA')
        uniqueIDS = Series(uniqueIDArray, name='lahmanID')
        df = concat([uniqueIDS, batAveS, plateAppearS], axis=1)
        df.sort(columns=batAveCol, ascending=False, inplace=True)
        df.to_csv(path_or_buf=Filepath.get_retrosheet_file(folder='unzipped', 
            subFolder='persistent', year=year), index=False)

    def __set_min_bat_ave(self):
        """
        Helper function for setup. Feeds off of __calc__players

        Produces the highest 3 digit float f such that for all P players 
        {p1, p2, .., pP}, pi_bat_ave >= f.
        """ 
        return self.players[-1].get_bat_ave()

# def main(*args, many=False):
#     """
#     run the simulation from the command line
#     """
#     if not many:
#         sim = NPSimulation(int(args[0]), int(args[1]), int(args[2]), int(args[3]))
#         sim.simulate()
#     # else, run a mass simulation
#     simYearRange = (int(args[0]), int(args[1]))
#     simMinBatRange = (int(args[2]), int(args[3]))
#     NRange = (int(args[4]), int(args[5]))
#     PRange = (int(args[6]), int(args[7]))
#     sim = NPSimulation(0, 0, 0, 0)
#     sim.many_simulate(simYearRange, simMinBatRange, NRange, PRange)

# if __name__ == '__main__':
#     """
#     Command line Usage:

#     1) ./npsimulation.py simYear batAveYear N P
#        -> runs a single simulation with given parameters
#     2) ./npsimulation.py simYearRange[0], simYearRange[1] simMinBatRange[0]
#               simMinBatRange[1] NRange[0] NRange[1] PRange[0] PRange[1] -m
#        -> runs a mass simulation with given parameters
#     """
#     if "-m" in sys.argv:
#         main(sys.argv, many=True)
#     else:
#         main(sys.argv)
#     main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
