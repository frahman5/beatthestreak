#! pyvenv/bin/python
import sys
import os
import pandas as pd
import datetime

from pandas import DataFrame, Series, ExcelWriter
from datetime import date, timedelta
from progressbar import ProgressBar
from progressbar.widgets import Timer, Percentage

from config import specialCasesD
from filepath import Filepath
from simulation import Simulation
from player import Player
from researcher import Researcher
from exception import DifficultYearException
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

    Currently only handles regular season.

    Notable Data:
        botHistoryBuffer: [date, ListOBots] where date is the date
        for which the buffer is buffering and ListOfBots is a list
        of bots that have received unique updates on the given date

    Special Cases:
        Suspended Games: In the event that a game was suspended and resumed on 
            a later date, NPSimulation recognizes it as a suspended game and
            considers it valid or invalid according to official 2014 beatthestreak
            rules. In the event that a game was suspended and NOT completed on
            a later date, NPSimulation considers it a normal game, which departs
            from official 2014 beatthestreak rules. This deviation only results 
            in undue endings to streaks, not undue elongations of streaks, 
            and is hence more conversative than beatthestreak rules.
        Mulligans: All robots start out with a "mulligan." Given a bot b, 
            the first time b reaches a streak length in [10,15] and chooses
            a player that fails to get a hit, the streak will be preserved. 
               [Note, offical MLB beatthestreak rules state bots need NOT
               be setup with mulligans to start. They can claim a mulligan
               at any point that its available.]
        Double Downs: On any given day, a bot is able to select two players. 
            Depending on the outcome of the players at bats, the bot's streak
            can either increase by 2, increase by 1, stay where it is, or 
            reset to 0
    """
    def __init__(self, simYear, batAveYear, N, P, startDate='default', 
            doubleDown=False, minPA=502):
        # _check_year type checks simYear and batAveYear
        assert type(N) == int
        assert type(P) == int
        
        Simulation.__init__(self, simYear, startDate)
        self.batAveYear = self._check_year(batAveYear)
        self.numBots = N
        self.numPlayers = P
        self.startDate = startDate
        self.minPA = minPA

        self.minBatAve = 0 # set upon setup
        self.players = [] # set upon setup
        self.bots = [] # set upon setup
        self.isSetup = False # # set upon setup
        self.susGamesDict = {} # set upon setup

        self.doubleDown = doubleDown
        self.botHistoryBuffer = [None, []]
        self.method = 1 # see NPReporter self.selMethods for what "1" means

        self.didNotRepeatSetup = False

    # @profile
    def setup(self):
        """
        Downloads necessary retrosheet data, initalizes bots, players, minBatAve, 
        susGamesDict
        """
        if self.isSetup: 
            self.didNotRepeatSetup = True # for testing
            return

        Simulation.setup(self) # download and parse retrosheet data
        self.bots = self._create_bots() # create N bots
        self.players = self.__calc__players(self.batAveYear, self.minPA) # create top P players
        self.minBatAve = self.__set_min_bat_ave() # store resultant min bat ave
        self.susGamesDict = Researcher.get_sus_games_dict(self.get_sim_year())
        for bot in self.bots:
            bot.claim_mulligan() # claim your mulligan baby
        self.isSetup = True
 
    # @profile
    def sim_next_day(self, doubleDown=False):
        """
        Bool -> None
        doubleDown: bool | Indicates whether or not bots should double down 
           every day


        Simulates the next day
        """
        assert type(doubleDown) == bool
        if doubleDown:
            self.__sim_next_day_double()
        else:
            self.__sim_next_day_single()
       
    def __sim_next_day_single(self):
        """
        None -> None

        Simulates the next day without using doubleDown strategies
        Helper function for sim_next_day
        """
        today = self.get_date()

        # Retrieve list of players playing today
        activePlayers = [player for player in self.players if \
             Researcher.did_start(today, player)]
        
        sGD = self.susGamesDict
        # assign players to bots and update histories
        modFactor = len(activePlayers)
        # no active players today
        if modFactor == 0: # pragma: no cover
            self.incr_date() 
            return
        for i, bot in enumerate(self.bots):
            player = activePlayers[i % modFactor]
            # Check if the desired info is on the buffer
            copyBot = self.__check_update_buffer(p1=player, p2=None, date=today)
            if copyBot:
                bot.update_history(bot=copyBot)
            else: # if its not, then update normally
                bot.update_history(p1=player, date=today, susGamesDict=sGD)
                self.botHistoryBuffer[1].append(bot)
        # update the date
        self.incr_date()

    # @profile
    def __sim_next_day_double(self):
        """
        None -> None

        Simulates the next day with doubleDown strategies
        Helper function for sim_next_day
        """
        today = self.get_date()

        # Retreve list of players playing today
        activePlayers = [player for player in self.players if \
            Researcher.did_start(today, player)]

        # assign players to bots and update histories
        modFactor = len(activePlayers)
        sGD = self.susGamesDict
        # no active Players today
        if modFactor == 0: # pragma: no cover
            self.incr_date() 
            return 
        for i, bot in enumerate(self.bots):
            if modFactor == 1: # can't double down if only 1 active player!
                p1 = activePlayers[0]
                # Check if desired info is on the buffer
                copyBot = self.__check_update_buffer(p1=p1, p2=None, date=today)
                if copyBot:
                    bot.update_history(bot=copyBot)
                else: # if its not, update normally
                    bot.update_history(p1=activePlayers[0], date=today, 
                        susGamesDict=sGD)
                    self.botHistoryBuffer[1].append(bot)
                continue
                
            ## Else double Down!
            # get player indices. Mod in p2Index accounts for odd Modfactor
            p1Index = (i * 2) % modFactor
            p2Index = (p1Index + 1) % modFactor 
            p1 = activePlayers[p1Index]
            p2 = activePlayers[p2Index]

            # Check if the desired info is on the buffer
            copyBot = self.__check_update_buffer(p1=p1, p2=p2, date=today)
            if copyBot:
                bot.update_history(bot=copyBot)
            else: # if its not, then update normally
                bot.update_history(p1=p1, p2=p2, date=today, susGamesDict=sGD)
                self.botHistoryBuffer[1].append(bot)

        # update the date
        self.incr_date()

    def __check_update_buffer(self, p1=None, p2=None, date=None):
        """
        player player date -> bot

        checks the bot update buffer to see if a bot has been assigned p1, p2
        on date date. If so, returns the bot. Else, returns None and
        updates the buffer if necessary
        """
        assert type(p1) == Player
        assert (p2 is None) or (type(p2)) == Player
        assert type(date) == datetime.date

        if self.botHistoryBuffer[0] == date:
            for bot in self.botHistoryBuffer[1]:
                if bot.get_players() == (p1, p2):
                    return bot
        else:
           self.botHistoryBuffer = [date, []] 
        return None

    # @profile 
    def simulate(self, numDays='max', anotherSim=False, test=False, prbar=True):
        """
        int|string  bool bool bool -> datetime.date datetime.date
        numDays: int|string | 'max' if simulation should run to closing day, 
            or an integer if simulation should run for a certain window of days
        anotherSim: bool | indicates whether or not another simulation will be 
            done using this object
        test: bool | indicates whether or not this is being run in a testing
           environment. For debugging
        prbar: indicates whether or not to display a progressbar

        returns startDate, lastDate (for reporting purposes)


        Simulates numDays number of days in self.simYear starting on 
        self.get_date(). Reports back the number of bots who achieved streaks
        of greater than 57, as well as their respective streak lengths. Reports
        back a variable number of top bots, inluding their player histories. 
        """
        assert (type(numDays) == str) or (type(numDays) == int)
        assert type(anotherSim) == bool
        assert type(test) == bool

        ## initalize relevant date variables and setup the simulation
        if self.startDate == 'default':
            self.currentDate = Researcher.get_opening_day(self.simYear)
        else:
            assert type(self.startDate) == datetime.date
            Researcher.check_date(self.startDate, startDate.year)
            self.currentDate = self.startDate
        startDate = self.currentDate
        self.currentDate = startDate
        lastDate = Researcher.get_closing_day(self.simYear)
        Reporter = NPReporter(self)
        self.setup()
 
        if prbar:
             # initialize a progressbar for the simulation
            maxVal = (lastDate - startDate).days # num Days in season
            if type(numDays) == int: 
                maxVal = numDays
            widgets = ['\nSIM: simYear: {0}'.format(
                self.get_sim_year()) + ", batAveYear: {0}".format(
                self.get_bat_year()) + " N: {0}, P: {1}. ".format(self.get_n(), 
                self.get_p()),  ' ', Percentage()]
            pbar = ProgressBar(maxval=maxVal, widgets=widgets).start()
            update_pbar = pbar.update

        # simulate days until lastDate reached or elapsedDays equals numDays
        elapsedDays = 0
        sim_next_day = self.sim_next_day
        doubleDown = self.doubleDown
        while True:
            if (numDays=='max') and (self.currentDate >= lastDate): # pragma: no cover
                Reporter.report_results(test=test, method=self.method)
                break
            if (type(numDays) == int) and elapsedDays >= numDays:
                Reporter.report_results(test=test, method=self.method)
                break
            sim_next_day(doubleDown=doubleDown)
            elapsedDays += 1
            if prbar:
                update_pbar(elapsedDays)
        if prbar:
            pbar.finish()

        # close up shop
        if anotherSim: # pragma: no cover
            self.set_setup(value=False)

        return startDate, lastDate

    def mass_simulate(self, simYearRange, simMinBatRange, NRange, PRange, 
            test=False):
        """
        tupleOfInts tupleOfInts tupleOfInts tupleOfInts bool -> None
        simYearRange: the years (inclusive) over which to run simulation
        simMinBatRange: the number of years (inclusive) over which to vary 
            simYear - batAveYear
        NRange: the integers (inclusive) over which to vary the number of bots
        PRange: the integers (inclusive) over which to vary top player calculations
        Test: bool | Indicates whether or not mass_simulate is being run 
           under a test framework. For debugging purposes

        For each year in simYearRange, for each batAveYear that results from
        subtracting a number in simMinBatRange from simYear, for each N in NRange, 
        take a P from P Range and run simulate. Report aggregate results in an 
        excel file. By default varies over doubleDown=True and doubleDown=False

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
        numSims = 0
        for param in (simYearRange, simMinBatRange, NRange, PRange):
            assert len(param) == 2
            for item in param:
                assert type(item) == int
        assert type(test) == bool


        # lists hold data that will later be written to .xlsxfile
        simYearL, batAveYearL, NL, PL , minBatAveL = [], [], [], [], []
        numSuccessL, percentSuccessL, numFailL, percentFailL = [], [], [], []
        minPAL, methodL, oneStreakL, twoStreakL, threeStreakL, = [], [], [], [], []
        fourStreakL, fiveStreakL, doubleDownL = [], [], []
        startDateL, endDateL = [], []

        # initialize a progressbar for the simulation
        maxval = len(range(simYearRange[0], simYearRange[1] + 1)) * \
                 len(range(simMinBatRange[0], simMinBatRange[1] + 1)) * \
                 len(range(NRange[0], NRange[1] + 1)) * \
                 len(range(PRange[0], PRange[1] + 1)) * 2
        widgets = ['\nMassSim: simYear:({0}, {1}), '.format(
            simYearRange[0], simYearRange[1]) + 'simMinBatRange({0}, {1}),'.format(
                simMinBatRange[0], simMinBatRange[1]) + ' N:({0}, {1}),'.format(
                NRange[0], NRange[1]) + ' P:({0}, {1}) '.format(
                PRange[0], PRange[1]), Timer(), ' ', Percentage()]
        pbar = ProgressBar(maxval=maxval, widgets=widgets).start()

        Reporter = NPReporter(self, test=test)
        # run all the simulations, saving individual simulation results to file
        i = 0
        for simYear in xrange(simYearRange[0], simYearRange[1]+1):
            for batAveYear in self.__bat_years_ms(simYear, simMinBatRange):
                for N in xrange(NRange[0], NRange[1]+1):
                    for P in xrange(PRange[0], PRange[1]+1):
                        for doubleDown in (True, False):
                            numSims += 1
                            # set sim parameters and simulate
                            self.set_sim_year(simYear)
                            self.set_bat_year(batAveYear)
                            self.set_n(N)
                            self.set_p(P)
                            self.doubleDown = doubleDown
                            print '\n    CurSim: {} {}'.format(self.simYear, 
                                self.batAveYear) + ' {} {} '.format(self.numBots, 
                                self.numPlayers) + ' dDown: {}'.format(self.doubleDown)
                            startDate, endDate = self.simulate(anotherSim=True, prbar=False)

                            # get 5 top streaks
                            self.get_bots().sort(key=lambda bot: bot.get_max_streak_length(), 
                                reverse=True)
                            fiveTopStreaks = [bot.get_max_streak_length() for bot 
                                in self.get_bots()][0:5]
                            if len(fiveTopStreaks) < 5: ## less than 5 bots!
                                for i in range(5):
                                    fiveTopStreaks.append('N/A')
                                    
                            # record sim metadata and results for later reporting
                            simYearL.append(self.get_sim_year())
                            batAveYearL.append(self.get_bat_year())
                            NL.append(self.get_n())
                            PL.append(self.get_p())
                            minBatAveL.append(self.get_min_bat_ave())
                            numS, percS, numF, percF = Reporter.calc_s_and_f()
                            numSuccessL.append(numS)
                            percentSuccessL.append(percS)
                            numFailL.append(numF)
                            percentFailL.append(percF)
                            minPAL.append(self.minPA)
                            methodL.append(self.method)
                            oneStreakL.append(fiveTopStreaks[0])
                            twoStreakL.append(fiveTopStreaks[1])
                            threeStreakL.append(fiveTopStreaks[2])
                            fourStreakL.append(fiveTopStreaks[3])
                            fiveStreakL.append(fiveTopStreaks[4])
                            doubleDownL.append(self.doubleDown)
                            startDateL.append(startDate)
                            endDateL.append(endDate)

                            # update progress bar
                            i += 1
                            pbar.update(i)
        pbar.finish() # kill the progress bar after the simulation ends

        # report aggregate results
        print "Reporting aggregate results to file"
        Reporter.report_mass_results(
            simYearL=simYearL, batAveYearL=batAveYearL, NL=NL, PL=PL, 
            minBatAveL=minBatAveL, numSuccessL=numSuccessL, 
            percentSuccessL=percentSuccessL, numFailL=numFailL, 
            percentFailL=percentFailL, oneStreakL=oneStreakL, 
            twoStreakL=twoStreakL, threeStreakL=threeStreakL, 
            fourStreakL=fourStreakL, fiveStreakL=fiveStreakL, 
            minPAL=minPAL, methodL=methodL, doubleDownL=doubleDownL,
            startDateL=startDateL, endDateL=endDateL,
            simYearRange=simYearRange, simMinBatRange=simMinBatRange, 
            NRange=NRange, PRange=PRange)

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

    def get_n(self):
        return self.numBots

    def get_p(self):
        return self.numPlayers

    def incr_date(self, num_days=1):
        """
        int -> None
        increment self.currentDate by num_days
        """
        self.currentDate += timedelta(days=num_days)

    def set_bat_year(self, batAveYear): # delete
        assert type(batAveYear) == int
        self.batAveYear = batAveYear

    def get_bat_year(self):
        return self.batAveYear

    def set_setup(self, value=False):
        self.isSetup = value

    def set_sim_year(self, simYear):
        assert type(simYear) == int
        self.simYear = simYear

    def set_n(self, N):
        assert type(N) == int
        self.numBots = N

    def set_p(self, P):
        assert type(P) == int
        self.numPlayers = P

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
            in range(simMinBatRange[1], simMinBatRange[0]-1, -1))
    # @profile
    def __calc__players(self, year, minPA):
        """
        int int -> ListOfTuples(player, player.bat_ave)

        Calculates the top P players with at least minPA plate appearances
        with respect to batting average in season year
        """
        self._check_year(year)

        # set initial variables
        minPA = minPA # minimum plate appearances to qualify for calculation
        players = []

        # check if the file with batting Averages for year year has
        # already been constructed, if not construct it
        if not os.path.isfile(Filepath.get_retrosheet_file(folder='persistent', 
            fileF='batAve', year=year)):
            self.__construct_bat_ave_csv(year) # pragma: no cover

        # Construct a list of the top P players
        df = DataFrame.from_csv(Filepath.get_retrosheet_file(folder='persistent', 
            fileF='batAve', year=year))
        lenPlayers, P = 0, self.get_p()
        append = players.append
        for lahmanID, batAve, PA in df.itertuples():
            if lenPlayers == P: # we've got all the players
                break
            if PA >= minPA: # make sure the player has enough plate appearances
                player = Player(lahmanID, year, batAve=batAve)
                append(player)
                # append(Player(lahmanID, year))
                lenPlayers += 1

        return players

    def __construct_bat_ave_csv(self, year): # pragma: no cover
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
        df = pd.read_csv(Filepath.get_lahman_file("Batting"), 
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
            player = Player(lahmanID, year)
            batAveList.append(player.get_bat_ave())
            plateAppearList.append(Researcher.num_plate_appearances(year, player))
            pbar.update(index)
        pbar.finish() # kill the proress bar

        # Write the data to csv
        batAveS = Series(batAveList, name=batAveCol)
        plateAppearS = Series(plateAppearList, name='PA')
        uniqueIDS = Series(uniqueIDArray, name='lahmanID')
        df = pd.concat([uniqueIDS, batAveS, plateAppearS], axis=1)
        df.sort(columns=batAveCol, ascending=False, inplace=True)
        df.to_csv(path_or_buf=Filepath.get_retrosheet_file(folder='persistent', 
            fileF='batAve', year=year), index=False)

    def __set_min_bat_ave(self):
        """
        Helper function for setup. Feeds off of __calc__players

        Produces the highest 3 digit float f such that for all P players 
        {p1, p2, .., pP}, pi_bat_ave >= f.
        """ 
        return self.players[-1].get_bat_ave()

def main(*args): # pragma: no cover
    """
    run a single or mass simulation from the command line
    """
    import re
    # see what special options the user wants
    options = [arg for arg in args if '-' in arg]

    # Set to default values, only changed if options included them
    massSim = False
    doubleDown = False
    minPA = 502

    # doubleDown?
    if '-d' in options:
        doubleDown = True
        print "If you're doing a mass simulation, then -d does nothing,"
        print "Mass simulation varies over single and double down by default"
    # non-standard minPA value?
    pMinPA = re.compile('-m=[1-9][0-9]+')
    matches = [pMinPA.match(option) for option in options if pMinPA.match(option)]
    if len(matches) == 1:
        minPA = int(matches[0].string[3:])
    elif len(matches) != 0:
        print "can only use the -m option once!"
        return
    # is it a normal or mass simulation?
    if '-M' in options:
        massSim = True
    if massSim:
        # make sure last four arguments are simYearLow-simYearHigh, 
        # batAveYearLow-batAveYearHigh, nLow-nHigh, pLow, pHigh
        numDashNumP = re.compile('[0-9]+-[0-9]+')
        for arg in args[-4:]:
            if numDashNumP.match(arg) == None:
                print "ERROR: Invalid arg: {}".format(arg)
        # get args and run simulation
        firstNumP = re.compile('^[0-9]+')
        lastNumP = re.compile('[0-9]+$')
        simYearLow = int(re.findall(firstNumP, args[-4] )[0])
        simYearHigh = int(re.findall(lastNumP, args[-4] )[0])
        smbLow = int(re.findall(firstNumP, args[-3] )[0])
        smbHigh = int(re.findall(lastNumP, args[-3] )[0])
        nLow = int(re.findall(firstNumP, args[-2] )[0])
        nHigh = int(re.findall(lastNumP, args[-2] )[0])
        pLow = int(re.findall(firstNumP, args[-1] )[0])
        pHigh = int(re.findall(lastNumP, args[-1] )[0])
        print "Mass Simming with sYR: {}-{}, smbR: {}-{}".format(simYearLow, 
            simYearHigh, smbLow, smbHigh) + \
            " nR: {}-{}, pR: {}-{}".format(nLow, nHigh, pLow, pHigh)
        print "Options: doubleDown: {}".format(doubleDown) 
        sim = NPSimulation(simYearLow, simYearHigh, nLow, pLow, 
                           doubleDown=doubleDown) 
        sim.mass_simulate((simYearLow, simYearHigh), 
                          (smbLow, smbHigh), 
                          (nLow, nHigh), (pLow, pHigh))
    else: # do a single simulation
        # make sure last four arguments are simYear, batAveYear, N, P
        for arg in args[-4:]:
            try:  
                int(arg)
            except ValueError as e:
                print e.message
                return
        sim = NPSimulation(int(args[-4]), int(args[-3]), int(args[-2]), 
                           int(args[-1]), doubleDown=doubleDown, minPA=minPA)
        print "Simming with simYear: {}, batAveYear: {}, N: {}, P: {}".format(
                int(args[-4]), int(args[-3]), int(args[-2]), int(args[-1]), minPA)
        print "Options: DoubleDown: {}, minPA: {}".format(doubleDown, minPA)
        sim.simulate()

if __name__ == '__main__': # pragma: no cover
    """
    Command line Usage:

    1) ./npsimulation.py simYear batAveYear N P
       -> runs a single simulation with given parameters
    2) ./npsimulation.py -d simYear batAveYear N P
       -> runs a single simulation with given parameters using DoubleDown
    3) ./npsimulation.py -d -m=minPA simYear batAveYear N P
       -> runs a single simulation with given parameters using doubleDown
       and minPA = minPA
    """
    main(*sys.argv)
    