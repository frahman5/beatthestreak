#! /usr/bin/python
import sys
import os
import pandas as pd
import datetime
import random

from pandas import DataFrame, Series, ExcelWriter
from datetime import date, timedelta
from progressbar import ProgressBar
from progressbar.widgets import Timer, Percentage

from cresearcher import cdid_start, copposing_pitcher_era
from config import specialCasesD
from filepath import Filepath
from simulation import Simulation
from player import Player
from researcher import Researcher
from exception import DifficultYearException, InvalidMethodException
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
            doubleDown=False, minPA=502, minERA=None, method=1):
        Simulation.__init__(self, simYear, startDate)
        self.batAveYear = self._check_year(batAveYear)
        self.numBots = N
        self.numPlayers = P
        self.startDate = startDate
        self.minPA = minPA
        self.minERA = minERA

        self.minBatAve = 0 # set upon setup
        self.players = [] # set upon setup
        self.bots = [] # set upon setup
        self.isSetup = False # # set upon setup

        self.doubleDown = doubleDown
           # default selection method
           # see NPReporter self.methods for definitions of methods
        self.method = method
   
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
        ## initalize relevant date variables and setup the simulation
        # if self.startDate == 'default':
        #     self.currentDate = Researcher.get_opening_day(self.simYear)
        # else:
        #     #assert type(self.startDate) == datetime.date
        #     Researcher.check_date(self.startDate, startDate.year)
        #     self.currentDate = self.startDate
        # startDate = self.currentDate
        # self.currentDate = startDate
        self.currentDate = date(self.simYear, 7, 7) # for actual production simulations
        startDate = self.currentDate
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
    
    # @profile
    def setup(self):
        """
        Downloads necessary retrosheet data, initalizes bots, players, minBatAve, 
        susGamesDict
        """
        if self.isSetup: 
            # self.didNotRepeatSetup = True # for testing
            return

        Simulation.setup(self) # download and parse retrosheet data
        self.bots = self._create_bots() # create N bots
        self.players = self.__calc__players(self.batAveYear, self.minPA) # create top P players
        self.__initalize_player_hit_info_csvs() # initalize their hit info csv's
        self.minBatAve = self.__set_min_bat_ave() # store resultant min bat ave
        # self.susGamesDict = Researcher.get_sus_games_dict(self.get_sim_year())
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
        if doubleDown:
            # print "SIMMED DOUBLE DOWN"
            self.__sim_next_day_double()
        else:
            # print "SIMMED SINGLE DOWN"
            self.__sim_next_day_single()
       
    def __sim_next_day_single(self):
        """
        None -> None

        Simulates the next day without using doubleDown strategies
        Helper function for sim_next_day
        """
        today = self.get_date()

        # Retrieve list of players qualifying today
        if self.method in (1, 2):
            # print "SELECTION: DID_START"
            qualifyingPlayers = [ player for player in self.players if \
                                  cdid_start(today, player.get_lahman_id()) ]
        elif self.method in (3, 4): 
            # print "SELECTION: DID_START and ERA > minERA"
            minERA = self.minERA
            qualifyingPlayers = [ 
                player for player in self.players if
                cdid_start(today, player.get_lahman_id()) and
                copposing_pitcher_era(player.get_lahman_id(), today) > minERA] 
        else:
            raise InvalidMethodException("Method: {} is not valid".format(
                        self.method))
        
        ## assign players to bots and update histories
        modFactor = len(qualifyingPlayers)
           # no active players today
        if modFactor == 0: # pragma: no cover
            self.incr_date() 
            return
            # deterministic distribution of players
        if self.method in (1, 3): 
            # print "DISTRIBUTION: DETERMINISTIC"
            for i, bot in enumerate(self.bots):
                player = qualifyingPlayers[i % modFactor]
                bot.update_history(p1=player, date=today)
            # random distribution of players
        elif self.method in (2, 4):
            # print "DISTRIBUTION: RANDOM"
            for bot in self.bots:
                player = random.choice(qualifyingPlayers)
                bot.update_history(p1=player, date=today)
        else: 
            raise InvalidMethodException("Method: {} is not valid".format(
                        self.method))

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

        ## Retrieve list of players qualifying today
        if self.method in (1, 2):
            # print "SELECTION: DID_START"
            qualifyingPlayers = [ player for player in self.players if \
                                  cdid_start(today, player.get_lahman_id()) ]
        elif self.method in (3, 4): 
            # print "SELECTION: DID_START and ERA > minERA"
            minERA = self.minERA
            qualifyingPlayers = [ 
                player for player in self.players if
                cdid_start(today, player.get_lahman_id()) and
                copposing_pitcher_era(player.get_lahman_id(), today) > minERA] 
        else:
            raise InvalidMethodException("Method: {} is not valid".format(
                        self.method))

        # assign players to bots and update histories
        modFactor = len(qualifyingPlayers)
        # no active Players today
        if modFactor == 0: # pragma: no cover
            self.incr_date() 
            return 
            # deterministic distribution
        if self.method in (1, 3):
            # print "DISTRIBUTION: DETERMINISTIC"
            for i, bot in enumerate(self.bots):
                if modFactor == 1: # can't double down if only 1 active player!
                    p1 = qualifyingPlayers[0]
                    bot.update_history(p1=p1, date=today)
                    continue
                    
                ## Else double Down!
                # get player indices. Mod in p2Index accounts for odd Modfactor
                p1Index = (i * 2) % modFactor
                p2Index = (p1Index + 1) % modFactor 
                p1 = qualifyingPlayers[p1Index]
                p2 = qualifyingPlayers[p2Index]
                # update bot
                bot.update_history(p1=p1, p2=p2, date=today)

            # random selection
        elif self.method in (2, 4):
            # print "DISTRIBUTION: RANDOM"
            for bot in self.bots:
                if modFactor == 1: # can't double down if only 1 active player!
                    p1 = random.choice(qualifyingPlayers)
                    bot.update_history(p1=p1, date=today)
                    continue
                ## Else double down
                p1 = random.choice(qualifyingPlayers)
                p2 = p1
                while (p2 == p1):
                    p2 = random.choice(qualifyingPlayers)
                # update bot
                bot.update_history(p1=p1, p2=p2, date=today)
        else:
            raise InvalidMethodException("Method: {} is not valid".format(
                        self.method))

        # update the date
        self.incr_date()

    def mass_simulate(self, simYearRange, simMinBatRange, NRange, PRange, 
            minPARange, minERARange=None, method=1, test=False):
        """
        tupleOfInts tupleOfInts tupleOfInts tupleOfInts tupleOfInts bool -> None
        simYearRange: the years (inclusive) over which to run simulation
        simMinBatRange: the number of years (inclusive) over which to vary 
            simYear - batAveYear
        NRange: the integers (inclusive) over which to vary the number of bots
        PRange: the integers (inclusive) over which to vary top player calculations
        minPARange: the inters (inclusive) over which to vary the minimum number
           of plate appearances that a player must have had to qualify for the competition. 
           We only iterate over every 5th PA.
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
        # lists hold data that will later be written to .xlsxfile
        simYearL, batAveYearL, NL, PL , minBatAveL = [], [], [], [], []
        numSuccessL, percentSuccessL, numFailL, percentFailL = [], [], [], []
        minPAL, methodL, oneStreakL, twoStreakL, threeStreakL, = [], [], [], [], []
        fourStreakL, fiveStreakL, topStreakAveL, doubleDownL = [], [], [], []
        percUniqueBotsL, startDateL, endDateL, minERAL = [], [], [], []

        # Get a tuple of tuples of simulation parameters
        params, numParams = self.__create_mass_sim_param_generator(
            simYearRange, simMinBatRange, NRange, PRange, minPARange, 
            minERARange=minERARange, method=method)

        # initialize a progressbar for the simulation
        minERAString = ''
        if method in (3,4):
            minERAString = 'minERA: ({}, {}) '.format( minERARange[0], 
                                                      minERARange[1])
        widgets = ['\nMassSim: simYear:({0}, {1}), '.format(
            simYearRange[0], simYearRange[1]) + 'simMinBatRange({0}, {1}),'.format(
                simMinBatRange[0], simMinBatRange[1]) + ' N:({0}, {1}),'.format(
                NRange[0], NRange[1]) + ' P:({0}, {1}) '.format(
                PRange[0], PRange[1]) + 'minPA:({0}, {1}) '.format(
                minPARange[0], minPARange[-1]) + minERAString + \
                ' Method: {} '.format(method) , Timer(), ' ', Percentage()]
        pbar = ProgressBar(maxval=numParams, widgets=widgets).start()
        
        Reporter = NPReporter(self, test=test)

        # run all the simulations, saving individual simulation results to file
        i = 0
        minERA = None
        for paramTuple in params:
            if method in (1,2):
                simYear, batAveYear, N, P, minPA, doubleDown = paramTuple
            elif method in (3,4):
                simYear, batAveYear, N, P, minPA, minERA, doubleDown = paramTuple
            else:
                raise ValueError("Invalid Method: {}\n".format(method))

            # set sim parameters and simulate
            self.set_sim_year(simYear)
            self.set_bat_year(batAveYear)
            self.set_n(N)
            self.set_p(P)
            self.doubleDown = doubleDown
            self.minPA = minPA
            self.method = method
            self.minERA = minERA
            startDate, endDate = self.simulate(anotherSim=True, prbar=False)

            # get 5 top streaks
            self.get_bots().sort(key=lambda bot: bot.get_max_streak_length(), 
                reverse=True)
            fiveTopStreaks = [bot.get_max_streak_length() for bot 
                in self.get_bots()][0:5]
            fiveTopStreakNums = [elem for elem in fiveTopStreaks] # for calcuating average
            while len(fiveTopStreaks) < 5:
                fiveTopStreaks.append('N/A')
                    
            # calculate num unique bots
            percentUniqueBots = round(
                float(Reporter._calc_num_unique_bots()) / float(N), 4)
            percentUniqueBotsString = "{0:.0f}%".format(100 * percentUniqueBots)

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
            percUniqueBotsL.append(percentUniqueBotsString)
            oneS, twoS, threeS, fourS, fiveS = fiveTopStreaks
            oneStreakL.append(oneS)
            twoStreakL.append(twoS)
            threeStreakL.append(threeS)
            fourStreakL.append(fourS)
            fiveStreakL.append(fiveS)
            topStreakAveL.append(float(sum(fiveTopStreakNums))/len(fiveTopStreakNums))
            doubleDownL.append(self.doubleDown)
            startDateL.append(startDate)
            endDateL.append(endDate)
            if minERA:
                minERAL.append(minERA)

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
            topStreakAveL=topStreakAveL, minPAL=minPAL, minERAL=minERAL,
            methodL=methodL, doubleDownL=doubleDownL, startDateL=startDateL, 
            endDateL=endDateL, percUniqueBotsL=percUniqueBotsL, 
            simYearRange=simYearRange, simMinBatRange=simMinBatRange, 
            NRange=NRange, PRange=PRange, minPARange=minPARange, 
            minERARange=minERARange)

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
        #assert type(batAveYear) == int
        self.batAveYear = batAveYear

    def get_bat_year(self):
        return self.batAveYear

    def set_setup(self, value=False):
        self.isSetup = value

    def set_sim_year(self, simYear):
        #assert type(simYear) == int
        self.simYear = simYear

    def set_n(self, N):
        #assert type(N) == int
        self.numBots = N

    def set_p(self, P):
        #assert type(P) == int
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
        for lahmanID, firstName, lastName, retrosheetID, batAve, PA in df.itertuples():
            if lenPlayers == P: # we've got all the players
                break
            if PA >= minPA: # make sure the player has enough plate appearances
                player = Player(lahmanID, year, batAve=batAve, 
                                firstName=firstName, lastName=lastName, 
                                retrosheetID=retrosheetID)
                append(player)
                # append(Player(lahmanID, year))
                lenPlayers += 1

        return players
    
    def __initalize_player_hit_info_csvs(self):
        """
        For each player in self.players, assures that the player hit info 
        csv has been written 
        """
        simYear = self.simYear
        for player in self.players:
            Researcher.create_player_hit_info_csv(player, simYear)

    # we don't cover this in test coverage because we don't want to have
    # to continually construct bat_avs_csvs. 
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

        # calculate batting averages, firstName, lastName, retrosheetID and plate appearances
        batAveList, plateAppearList = [], []
        firstNameList, lastNameList = [], []
        retrosheetIDList = []
        for index, lahmanID in enumerate(uniqueIDArray):
            player = Player(lahmanID, year)
            batAveList.append(player.get_bat_ave())
            plateAppearList.append(Researcher.num_plate_appearances(year, player))
            firstNameList.append(player.get_first_name())
            lastNameList.append(player.get_last_name())
            retrosheetIDList.append(player.get_retrosheet_id())
            pbar.update(index)
        pbar.finish() # kill the proress bar

        # Write the data to csv
        batAveS = Series(batAveList, name=batAveCol)
        firstNameS = Series(firstNameList, name='FirstName')
        lastNameS = Series(lastNameList, name='LastName')
        retrosheetIDS = Series(retrosheetIDList, name='RetrosheetID')
        plateAppearS = Series(plateAppearList, name='PA')
        uniqueIDS = Series(uniqueIDArray, name='lahmanID')
        df = pd.concat([uniqueIDS, firstNameS, lastNameS, 
                        retrosheetIDS, batAveS, plateAppearS], axis=1)
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

    def __create_mass_sim_param_generator(self, simYearRange, simMinBatRange, 
            NRange, PRange, minPARange, minERARange=None, method=1):
        """
        Produces a Tuple of parameter-tuples to use in a mass simulation, 
           and the number of elems in that generator
        """
        if method in (1,2):
            paramGenerator = (
                (simYear, batAveYear, N, P, minPA, dDown) for
                  simYear in xrange(simYearRange[0], simYearRange[1] + 1) for
                  batAveYear in self.__bat_years_ms(simYear, simMinBatRange) for 
                  N in self.__get_param_range(NRange[0], NRange[1], 10) for 
                  P in self.__get_param_range(PRange[0], PRange[1], 5)  for 
                  minPA in self.__get_min_pa_range(minPARange[0], minPARange[1]) for 
                  dDown in (True, False) 
                             )
        elif method in (3, 4):
            paramGenerator = (
                (simYear, batAveYear, N, P, minPA, minERA, dDown) for
                  simYear in xrange(simYearRange[0], simYearRange[1] + 1) for
                  batAveYear in self.__bat_years_ms(simYear, simMinBatRange) for 
                  N in self.__get_param_range(NRange[0], NRange[1], 10) for 
                  P in self.__get_param_range(PRange[0], PRange[1], 5)  for 
                  minPA in self.__get_min_pa_range(minPARange[0], minPARange[1]) for 
                  minERA in self.__get_min_era_range( minERARange[0], 
                                                      minERARange[1]) for 
                  dDown in (True, False) 
                             )
        else:
            raise ValueError("Invalid method: {}".format(method))
        
        paramTuple = tuple(paramGenerator)
        return paramTuple, len(paramTuple)

    def __get_min_pa_range(self, minPALow, minPAHigh):
        """
        int int -> tuple

        Returns a tuple that contains:
           minPALow, MinPALow + 100, minPALow + 200, ..., miNPAHigh)
        """
        return self.__get_param_range(minPALow, minPAHigh, 100)

    def __get_min_era_range(self, minERALow, minERAHigh):
        """
        float float -> tuple

        Returns a tuple that contains:
           ( minERALow, minERALow + 0.5, minERALow + 1.0, ..., minERAHigh )
        """
        return self.__get_param_range(minERALow, minERAHigh, 0.5)

    def __get_param_range(self, paramLow, paramHigh, step):
        """
        int|float int|float int|float -> tuple

        Returns a tuple that contains
            (minParamLow, minParamLow + step, minParamLow + 2*step , ..., minParamHigh)
        """
        if paramLow == paramHigh:
            return (paramLow, )
        else:
            preAnswer = []
            param = paramLow
            while param <= paramHigh:
                preAnswer.append(param)
                param += step
        if preAnswer[-1] != paramHigh:
            preAnswer.append(paramHigh)
        return tuple(preAnswer)



def main(*args): # pragma: no cover
    """
    run a single or mass simulation from the command line
    """
    import re

    ## see what special options the user wants
    options = [arg for arg in args if '-' in arg]

        # Set to default values, only changed if options included them
    doubleDown = False
    minPA = 502
    simMethod = 1

        # doubleDown?
    if '-d' in options:
        doubleDown = True
        options.remove('-d')

        # non-standard minPA value?
    pMinPA = re.compile(r"""
        -mP=            # minPlateAppearnces setting option
        [1-9]           # 1 non-zero digit
        [0-9]+          # 1 or more digits
        """, re.VERBOSE)
    matches = [pMinPA.match(option) for option in options if pMinPA.match(option)]
    if len(matches) == 1:
        minPA = int(matches[0].string[3:])
        options.remove(matches[0].string)
    elif len(matches) != 0:
        print "can only use the -m option once!"
        return

        # which sim method do we use? If it's 3 or 4, what's the minERA?
    pSimMethod = re.compile(r"""
        -sM=            # sim Method setting option
        [1-4]           # method number must be in (1, 2, 3, 4)
        """, re.VERBOSE)
    matches = [ pSimMethod.match(option) for option in options if 
                pSimMethod.match(option)]
    if matches:
        simMethod = int(matches[0].string[-1])
        options.remove(matches[0].string)
    if simMethod in (3, 4):
        pMinERA = re.compile(r"""
            -mE=        # minERA setting option 
            [0-9]+      # 1 or more digits
            .?          # 0 or 1 decimal points
            [0-9]*      # 0 or more digits
            """, re.VERBOSE)
        matches = [ pMinERA.match(option) for option in options if 
                    pMinERA.match(option)]
        assert matches[0]
        minERA = float(matches[0].string.partition('=')[-1])
        options.remove(matches[0].string)
    else:
        minERA = None

        # is it a test or a full run?
    testOption = '-t'
    if testOption in options:
        test=True
        options.remove(testOption)
    else: 
        test=False

    ## Check that last four arguments--simYear, batAveYear, N, P-- are ints
    for arg in args[-4:]:
        try:  
            int(arg)
        except ValueError as e:
            raise e

    ## Check that we didn't get any bogus options:
    if len(options) != 0:
        raise KeyError("Invalid options: " + str(options))

    ## Run the simulation
    sim = NPSimulation(int(args[-4]), int(args[-3]), int(args[-2]), 
                       int(args[-1]), doubleDown=doubleDown, minPA=minPA, 
                       method=simMethod)
    sim.minERA = minERA
    print "Simming with simYear: {}, batAveYear: {}, N: {}, P: {}".format(
            int(args[-4]), int(args[-3]), int(args[-2]), int(args[-1]), minPA)
    print "Options. DoubleDown: {}, minPA: {}, simMethod: {}, minERA: {}".format(
              doubleDown, minPA, simMethod, minERA) 
    sim.simulate(test=test)

if __name__ == '__main__': # pragma: no cover
    """
    Command line Usage:

    1) ./npsimulation.py [OPTIONS] simYear batAveYear N P
       -> runs a single simulation with given parameters and options

    Options:
       -d : DoubleDown. If not provided, default is SingleDown
       -sM=[METHODNUMBER]: Indicate simulation method. METHODNUMBER is an int
                           If -sM=3 or -sM=4 is chosen, must provide -mE
       -mE=[MINERA]: Indicate minimum era to be used if sM=3 or sM=4. Must be 
                     a positive rational number.
       -mP=[minPlateAppearnces]: Indicate minimum number of plate appearances
                                 that a player must have had to qualify for the sim
                                 If not provided, defaults to 502
       -t : indicates results should be printed to test results folder
    """
    main(*sys.argv)
    
