#! pyvenv/bin/python

from simulation import Simulation
import pandas as pd
import sys
import os

from data import Data
from pandas import DataFrame, Series, ExcelWriter
from datetime import date, timedelta
from progressbar import ProgressBar
from progressbar.widgets import Timer, Percentage
from player import PlayerL, Player
from researcher import Researcher
from exception import DifficultYearException
from bot import Bot

class NPSimulation(Simulation):
    """
    A BTS simulation using the NP strategy. 

    NP Strategy denotes a number N of robots and a number P of MLB players. 

    Strategy: The Simulation initalizes N robots (accounts) and calculates the P
    "best" players ordered by highest seasonal or career batting average. Each
    day, it checks which of the P players are playing in a game and then assigns
    the active ones to the bots in order from highest batting average to lowest, 
    repeating the list of P players as many times as needed to assign a player
    to every bot. 

    Currently only handles regular season
    """
    def __init__(self, simYear, batAveYear, N, P, startDate='default'):
        Simulation.__init__(self, simYear, startDate)
        self.simYear = self._check_year(simYear)
        self.batAveYear = self._check_year(batAveYear)
        self.numBots = N
        self.numPlayers = P
        self.minBatAve = 0 # set later, upon setup
        self.players = [] # set later, upon setup
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
        self.bots = self._create_bots() # create N bots
        self.players = self.__calc__players(self.batAveYear) # get P top players
        self.minBatAve = self.__set_min_bat_ave() # store resultant min bat ave
        self.isSetup = True

    def sim_next_day(self):
        """
        None -> None

        Simulates the next day
        """
        yesPrint = False
        if self.get_date() == date(2013, 5, 27):
            yesPrint = True
        print "Simming day: {0}".format(self.get_date())
        # which players were active?
        activePlayers = [player for player in self.players if \
             Researcher.did_start(self.currentDate, player)]
        # assign players to bots
        mod_factor = len(activePlayers)
        if mod_factor == 0:
            self.incr_date()
            return # no activePlayers today
        for i, bot in enumerate(self.bots):
            player = activePlayers[i % mod_factor]
            if yesPrint: print player
            bot.assign_player(player, 
                Researcher.did_get_hit(self.currentDate, player), self.currentDate)
            if yesPrint: print "we got past the assignment"
        # update the date
        self.incr_date()
    
    def simulate(self, numDays='max', anotherSim=False, resultsMethod='excel'):
        """
        int|string  bool string-> None
        numDays: 'max' if simulation should run to closing day, or an integer
            if simulation should run for a certain window of days
        anotherSim: indicates whether or not another simulation will be done 
            using this object
        resultsMethod: ('stdout', 'excel'). Indicates preferred method of results
            output


        Simulates numDays number of days in self.simYear, starting on 
        self.startDate. Reports back the number of bots who achieved streaks
        of greater than 57, as well as their respective streak lengths. No 
        matter what, reports back at least the 5 best streaks, including
        player histories
        """
        startDate = self.currentDate
        lastDaySeason = Researcher.get_closing_day(self.simYear)
        elapsedDays = 0

        self.setup()
        while True:
            if (numDays=='max') and (self.currentDate > lastDaySeason):
                self.report_results()
                break
            if (type(numDays) == int) and elapsedDays >= numDays:
                self.report_results()
                break
            self.sim_next_day()
            elapsedDays += 1
        
        if anotherSim:
            self.set_setup(value=False)
        else:
            self.close() # cleans up retrosheet files from harddrive
        
        print "Simulation simYear: {1}, batAveYear: {2} ".format(
            self.get_sim_year(), self.get_bat_year()) + \
            "N: {1}, P: {2} over!".format(self.get_n(), self.get_p())

    def many_simulate(self, simYearRange, simMinBatRange, NRange, 
        PRange):
        """
        tupleOfInts tupleOfInts tupleOfInts tupleOfInts -> None
        simYearRange: the years (inclusive) over which to run a simulation
        simMinBatRange: the number of years (inclusive) over which to vary 
        simYear - batAveYear
        NRange: the integers (inclusive) over which to vary the number of bots
        PRange: the integers (inclusive) over which to vary top player calculations

        For each year in simYearRange, for each batAveYear that results from
        subtracting a number in simMinBatRange from simYear, for each N in NRange, 
        take a P from P Range and run simulate. Report aggregate results in a csv
        file.

        e.g: sim.many_simulate((2010,2010), (0,1), (1,2), (1,2)) runs a simulation
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
        simYearL, batAveYearL, NL, PL , minBatAveL = [], [], [], [], []
        numSuccessL, percentSuccessL, numFailL, percentFailL = [], [], [], []

        maxval = len(range(simYearRange[0], simYearRange[1] + 1)) * \
                 len(range(simMinBatRange[0], simMinBatRange[1] + 1)) * \
                 len(range(NRange[0], NRange[1] + 1)) * \
                 len(range(PRange[0], PRange[1] + 1))
        widgets = ['Running simulations with simYear:({0}, {1}), '.format(
            simYearRange[0], simYearRange[1]) + 'simMinBatRange({0}, {1}'.format(
                simMinBatRange[0], simMinBatRange[1]), + ' N:{0} , P: {1}'.format(
                self.get_n(), self.get_p()), Timer(), ' ', Percentage()]
        pbar = ProgressBar(maxval=maxval, widgets=widgets).start()
        ## run all the simulations, saving results to file for those simulations
        ## with progressbar
        i = 0
        for simYear in simYearRange:
            for batAveYear in self._bat_years_ms(simYear, simMinBatRange):
                for N in NRange:
                    for P in PRange:
                        # set sim parameters and simulate
                        self.set_sim_year(simYear)
                        self.set_bat_year(batAveYear)
                        self.set_n(N)
                        self.set_p(P)
                        self.simulate(anotherSim=True)

                        # record sim results for reporting
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
        pbar.finish()

        ## report aggregate results
        self._report_many_results_excel(simYearL, batAveYearL, NL, PL, 
            minBatAveL, numSuccessL, percentSuccessL, numFailL, percentFailL, 
            simYearRange, simMinBatRange, NRange, PRange)

        self.close()

    def calc_s_and_f(self):
        """
        None -> int float int float

        Returns numSuccesses, percentSuccesses, numFailures, percentFailures
        for a completed simulation (self). 
        """
        # calculate num_successes
        numSuccesses = 0
        for bot in self.get_bots():
            if bot.get_max_streak_length() >= 57:
                numSuccesses += 1

        numFailures = self.get_n() - numSuccesses
        percentSuccesses = round(float(numSuccesses)/float(self.get_n()), 3)
        percentFailures = round(float(numFailures)/float(self.get_n()), 3)

        return numSuccesses, percentSuccesses, numFailures, percentFailures

    def _report_many_results_excel(simYearL, batAveYearL, NL, PL, 
            minBatAveL, numSuccessL, percentSuccessL, numFailL, percentFailL, 
            simYearRange, simMinBatRange, NRange, PRange):
        """
        list list list list list list list list list tupleOfInts
            tupleOfInts tupleOfInts tupleOfInts -> None
        simYearL: List of simulation years for mass simulation
        batAveYearL: List of batting average years for mass simulation
        NL: List of N values for mass simulation
        PL: List of P values for mass simulation
        minBatAveL: list of minBatAve values for mass simulation
        numSuccessL: List of number of Successes for mass simulation
        percentSuccessL: List of percent of successes for mass simulation
        numFailL: list of number of failrues for mass simulation
        percentFailL: list of percent failures for mass simulation
        simYearRange: (lowest_sim_year, highest_sim_year)
        simMinBatRange: (lowest simYear-batAveYear, highest simYear-batAveYear)
        NRange: (lowest N, highest N)
        PRange: (lowest P, highset P)

        Reports mass simulation results to excel spreadsheet
        """
        # Create dataframe with results
        d = {'Sim Year': simYearL, 'Bat Ave Year': batAveYearL, 'N': NL, 
             'P': PL, 'Min Bat Ave': minBatAveL, 'Successes': numSuccessL, 
             'Successes (%)': percentSuccessL, 'Failures': numFailL, 
             'Failures (%)': percentFailL }
        df = DataFrame(d)

        # Write the info to an excel spreadsheet
        writer = ExcelWriter(Data.get_mass_results_path(simYearRange, 
            simMinBatRange, NRange, PRange))
        df.to_excel(writer=writer, index=False, sheet_name='Meta')
        writer.save()

    def report_results(self, method='excel'):
        """
        string -> None
        method: string ('stdout', 'excel') indicating the output method for results

        Reports simulation results
        """
        if method == 'stdout':
            self._report_results_stdout()
        if method == 'excel':
            self._report_results_excel()

    def _bat_years_ms(self, simYear, simMinBatRange):
        """
        int tupleOfInts -> generatorOfInts
        simYear: year of simulation (four digit int)
        simMinBatRange: a duple (minYearsToSubtractFromSimYear,
                                 maxYearsToSubtractFromSimYear)
        """
        ## type checking 
        assert (type(simYear) == int) and (simYear >= 1900)
        assert (type(simMinBatRange) == tuple)
        for item in simMinBatRange:
            assert type(item) == int

        ## logic 
        return (simYear - difference for difference 
            in range(simMinBatRange[0], simMinBatRange[1] + 1))

    def _calc_num_unique_bots(self):
        """
        None -> int
        Returns the number of bots with unique player histories
        """
        N = self.get_n()
        numUnique = N
        bots = self.get_bots()
        for index, bot in enumerate(bots):
            for j in range(index+1, N):
                if bot == bots[j]:
                    numUnique -= 1
                    break
        return numUnique
        
    def __calc__players(self, year):
        """
        None -> ListOfTuples(player, player.bat_ave)
        Calculates the top P players with respect to batting average
        in season self.batBatAveYear
        """
        assert type(year) == int

        minPA = 502 # minimum plate appearances to qualify for calculation
        players = []

        if not os.path.isfile(Data.get_persistent_bat_ave_file(year)):
            self._construct_bat_ave_csv(year)

        # get the data from csv
        df = pd.DataFrame.from_csv(Data.get_persistent_bat_ave_file(year))

        # calculate the top P players, with progressbar
        widgets = \
            ['    Calculating the top {0} players in year {1} from file '.format(
            self.get_p(), self.get_bat_year()), Timer(), ' ', Percentage()]
        pbar = ProgressBar(maxval=self.get_p(), widgets=widgets).start()

        lenPlayers, P = 0, self.get_p()
        for lahmanID, batAve, PA in df.itertuples():
            if lenPlayers == P:
                break
            if PA >= minPA:
                players.append(Player(lenPlayers, 
                    playerL=PlayerL(lahmanID, year)))
                lenPlayers += 1
                pbar.update(lenPlayers)
        pbar.finish()
        return players

    def _construct_bat_ave_csv(self, year):
        """
        year -> None

        Produces a csv with lahmanIDs and corresponding batting averages
        in year year, sorted by batting average column. Saves it to 
        file. Helper function for _calc_players
        """
        batAveCol = 'batAve' + str(year) + 'Sorted'
        
        # get series of unique playerIDs corresponding to given year
        df = pd.read_csv(Data.get_lahman_path("Batting"), 
                           usecols=['playerID', 'yearID', 'AB'])
        df = df[df.yearID == year]
        uniqueIDArray = pd.Series(df.playerID.values.ravel()).unique()
             # uniqueIDArray is of type ndarray

        # calculate batting averages, plate appearances, with progressbar
        widgets = ['     Creating batting average csv for year %s ' % year, 
            Timer(), ' ', Percentage()]
        pbar = ProgressBar(maxval=len(uniqueIDArray), widgets=widgets).start()

        batAveList, plateAppearList = [], []
        for index, lahmanID in enumerate(uniqueIDArray):
            pbar.update(index) # progress tracker
            player = PlayerL(lahmanID, year)
            batAveList.append(player.get_bat_ave())
            plateAppearList.append(
                Researcher.num_plate_appearances(year, player))
        pbar.finish()

        # persist the data in a csv
        batAveS = pd.Series(batAveList, name=batAveCol)
        plateAppearS = pd.Series(plateAppearList, name='PA')
        uniqueIDS = pd.Series(uniqueIDArray, name='lahmanID')
        df = pd.concat([uniqueIDS, batAveS, plateAppearS], axis=1)
        df.sort(columns=batAveCol, ascending=False, inplace=True)
        df.to_csv(path_or_buf=Data.get_persistent_bat_ave_file(year), 
            index=False)

    def _report_results_stdout(self):
        """
        Prints out results for the simulation. Includes:
            1) Simulation year, N value, P Values
            2) Simulation start and end dates
            3) Simulation batting ave calculation method and minimum value
            4) 2-5 best bots/streaks, including player history (with date info
            included) over their best streaks
        """
        startDate = self.get_bots()[0].get_history()[0][2]
        space5 = "     "
        space10 = "          "
        space12 = "            "

        # calculate best bots
        self.get_bots().sort(key=lambda bot: bot.get_max_streak_length())
        self.get_bots().reverse()
        bestBots = self.get_bots()

        # print header
        print "****************************************************************"
        print "Simulation {0}. N: {1}, P: {2}, {3} to {4}".format(self.get_sim_year(), 
            self.get_n(), self.get_p(), startDate, self.get_date())
        
        # print success/failure reporting
        if bestBots[0].get_max_streak_length() >= 57:
            num_successes = 0
            while bestBots[num_successes].get_max_streak_length() >= 57:
                num_successes += 1
            print "     SUCCESS: {0} bot(s) beat the streak!".format(num_successes)
        else:
            print "     FAILURE: No bots beat the streak :("
        
        # Data report
        print space5 + "Minimum Batting Average: {0}".format(self.get_min_bat_ave())
        print space10 + "Calculation method: Seasonal, year {0}".format(self.get_bat_year())
        print space5 + "Five best bots:"
        for bot in bestBots[0:2]:
            print space10 + "Bot {0}. Max Streak Length: {1}".format(bot.get_index(), 
                bot.get_max_streak_length())
            print space12 + "                  Player|  Hit  |    Date    | Streak_length"
            for day in bot.get_history():
                print space12 + str(day[0]).rjust(24), # player
                print str(day[1]).rjust(7), # True|False for hit
                print str(day[2]).rjust(12),# Date
                print str(day[3]).rjust(7)  # Streak length on given date
        print "****************************************************************"

    def _report_results_excel(self):
        """

        Produces results of a simulation in a csv file
        """
        numTopBots = 2
        startDate = self.get_bots()[0].get_history()[0][2]
        endDate = self.get_bots()[0].get_history()[-1][2]
        writer = ExcelWriter(Data.get_results_path(self.get_sim_year(), 
            self.get_bat_year(), self.get_n(), self.get_p(), startDate, endDate))

        # calculate best bots
        self.get_bots().sort(key=lambda bot: bot.get_max_streak_length())
        self.get_bots().reverse()
        bestBots = self.get_bots()

        # report results for top performing bots
        for bot in bestBots[0:numTopBots]:
            self._report_bot_results_to_excel(bot, writer)

        # report bots metadata
        self._report_bots_metadata_results_excel(writer)

        # report sim metadata
        self._report_sim_metadata_results_excel(writer)

        # save everthing to file
        writer.save()

    def _report_bot_results_to_excel(self, bot, writer):
        """
        bot ExcelWriter -> None
        bot: the bot for which you want to report results
        ExcelWriter: an excelWriter object

        Outputs bot info results to excel buffer. Helper function for 
        _report_results_excel
        """
        history = bot.get_history()
        playerS = Series([event[0].get_name() for event in history], 
            name='Player')
        batAveS = Series([event[0].get_bat_ave() for event in history], 
            name='Batting Average')
        hitS = Series([event[1] for event in history], name='Hit')
        dateS = Series([event[2] for event in history], name='Date')
        streakS = Series([event[3] for event in history], 
            name='Streak Length')

        # construct dataframe to write to excel file
        df = pd.concat([playerS, batAveS, hitS, dateS, streakS], axis=1)

        # put df info on excel buffer
        botIndexString = str(bot.get_index())
        botLongestStreak = str(bot.get_max_streak_length())
        df.to_excel(writer, index=False,
            sheet_name='bot' + botIndexString + '-' + botLongestStreak)

    def _report_bots_metadata_results_excel(self, writer):
        """
        writer -> None
        """
        enoughEmptyRows = ["" for i in range(self.get_n()-1)]
        percentUniqueBots = round(
            float(self._calc_num_unique_bots()) / float(self.get_n()), 4)
        percentUniqueBotsString = "{0:.0f}%".format(100 * percentUniqueBots)

        # takes advantage of fact that bots are already sorted by streak length
        botS = Series([bot.get_index() for bot in self.get_bots()], name='Bot')
        maxStreakS = Series([bot.get_max_streak_length() for bot in \
            self.get_bots()], name='maxStreak')
        aveStreakS = Series([maxStreakS.mean()] + enoughEmptyRows, 
            name="aveMaxStreak")
        uniqueBotS = Series([percentUniqueBotsString] + \
            enoughEmptyRows, name='Unique Bots(%)')

        # construct dataframe to write to excel file
        df = pd.concat([botS, maxStreakS, aveStreakS, uniqueBotS], axis=1)

        # put df info on excel buffer
        df.to_excel(writer, index=False, sheet_name='Bots Meta')

    def _report_sim_metadata_results_excel(self, writer):
        """
        writer -> None
        """
        # get number, percent of success
        numSuccesses, perecentSuccesses, numFails, percentFails = \
            self.calc_s_and_f()
        percentSuccessesString = "{0:.0f}%".format(100 * percentSuccesses)

        yearS = Series([self.get_sim_year()], name='simYear')
        batS = Series([self.get_bat_year()], name='batAveYear')
        nS = Series([self.get_n()], name='N')
        pS = Series([self.get_p()], name='P')
        startDateS = Series([self.get_bots()[0].get_history()[0][2]], 
            name='startDate')
        endDateS = Series([self.get_bots()[0].get_history()[-1][2]], 
            name='endDate')
        successS = Series([numSuccesses], name='numSuccesses')
        percentSuccessS = Series([percentSuccessesString], 
            name='percentSuccesses')

        # construct dataframe to write to excel file
        df = pd.concat([yearS, batS, nS, pS, startDateS, endDateS, 
            successS, percentSuccessS], axis=1)

        # put df info on excel buffer
        df.to_excel(writer, index=False, sheet_name='Sim Meta')

    def __set_min_bat_ave(self):
        """
        Helper function for setup. Feeds off of __calc__players

        Produces the highest 3 digit float f such that for all P players 
        {p1, p2, .., pP}, pi_bat_ave >= f.
        """ 
        return self.players[-1].get_bat_ave()

    def _check_year(self, year):
        """
        int -> None|int
        Produces an exception if year is before 1962 or a strike year (1972, 
            1982, 1994, 1995) since 1962. Returns the given year otherwise.
        """
        assert type(year) == int
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
    
    def set_sim_year(self, year):
        self.simYear = year

    def get_sim_year(self):
        return self.simYear

    def set_bat_year(self, year):
        self.batAveYear = year

    def get_bat_year(self):
        return self.batAveYear

    def set_setup(self, value=False):
        self.isSetup = value

    def get_setup(self):
        return self.isSetup

def main(*args, many=False):
    """
    run the simulation from the command line
    """
    if not many:
        sim = NPSimulation(int(args[0]), int(args[1]), int(args[2]), int(args[3]))
        sim.simulate()
    # else, run a mass simulation
    simYearRange = (int(args[0]), int(args[1]))
    simMinBatRange = (int(args[2]), int(args[3]))
    NRange = (int(args[4]), int(args[5]))
    PRange = (int(args[6]), int(args[7]))
    sim = NPSimulation(0, 0, 0, 0)
    sim.many_simulate(simYearRange, simMinBatRange, NRange, PRange)

if __name__ == '__main__':
    """
    Command line Usage:

    1) ./npsimulation.py simYear batAveYear N P
       -> runs a single simulation with given parameters
    2) ./npsimulation.py simYearRange[0], simYearRange[1] simMinBatRange[0]
              simMinBatRange[1] NRange[0] NRange[1] PRange[0] PRange[1] -m
       -> runs a mass simulation with given parameters
    """
    if "-m" in sys.argv:
        main(sys.argv, many=True)
    else:
        main(sys.argv)
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
