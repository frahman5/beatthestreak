from pandas import ExcelWriter, Series, DataFrame, concat
from pandas.io.excel import _OpenpyxlWriter # for type checking

from filepath import Filepath
from bot import Bot

class NPReporter(object):
    """
    NPReporter initalizes with an instance of NPSimulation and is used
    to report simulation results
    """
    
    def __init__(self, npsim, Test=False):
        """
        NPSimulation bool -> None
        npsim: NPSimulation | the simulation for which this reporter object will 
           report results
        Test: bool | Indicates whether or not this Reporter is reporting under
           a testing framework. For debugging purposes
        """
        self.npsim = npsim
        self.outputMethods = ('excel', 'stdout')
        self.Test=Test

    def get_npsim(self):
        return self.npsim

    def report_results(self):
        """
        None -> None

        Produces results of self.npsim in an excel file
        """
        npsim = self.get_npsim()
        # Initalize variables

        numTopBots = 2 # number of top bot histories to report
        startDate = npsim.get_bots()[0].get_history()[0][4]
        endDate = npsim.get_bots()[0].get_history()[-1][4]
        writer = ExcelWriter(Filepath.get_results_file(npsim.get_sim_year(), 
            npsim.get_bat_year(), npsim.get_n(), npsim.get_p(), startDate, endDate))

        # calculate best bots
        npsim.get_bots().sort(key=lambda bot: bot.get_max_streak_length())
        npsim.get_bots().reverse()
        bestBots = npsim.get_bots()

        # report results for top performing bots
        for bot in bestBots[0:numTopBots]:
            self.__report_bot_results_to_excel(bot, writer)

        # report bots metadata
        self.__report_bots_metadata_results_excel(writer)

        # report sim metadata
        self.__report_sim_metadata_results_excel(writer)

        # save everthing to file
        writer.save()

    def report_mass_results(**kwargs):
        """
        simYearL: List of simulation years for mass simulation
        batAveYearL: List of batting average years for mass simulation
        NL: List of N values for mass simulation
        PL: List of P values for mass simulation
        minBatAveL: list of minBatAve values for mass simulation
        numSuccessL: List of number of Successes for mass simulation
        percentSuccessL: List of percent of successes for mass simulation
        numFailL: list of number of failures for mass simulation
        percentFailL: list of percent failures for mass simulation
        simYearRange: (lowest_sim_year, highest_sim_year)
        simMinBatRange: (lowest simYear-batAveYear, highest simYear-batAveYear)
        NRange: (lowest N, highest N)
        PRange: (lowest P, highset P)

        Reports mass simulation results to excel spreadsheet
        """
        npsim = self.get_npsim()
        for item in kwargs.itervalues():
            assert type(item) == list

        # Create dataframe with results
        d = {'Sim Year': kwargs['simYearL'], 'Bat Ave Year': kwargs['batAveYearL'], 
             'N': kwargs['NL'], 'P': kwargs['PL'], 'Min Bat Ave': kwargs['minBatAveL'], 
             'Successes': kwargs['numSuccessL'], 
             'Successes (%)': kwargs['percentSuccessL'], 
             'Failures': kwargs['numFailL'], 'Failures (%)': kwargs['percentFailL'] }
        df = DataFrame(d)

        # Write the info to an excel spreadsheet
        if self.Test == True: # debugging code
            writer = ExcelWriter(Filepath.get_mass_results_file(
                kwargs['simYearRange'], kwargs['simMinBatRange'], 
                kwargs['NRange'], kwargs['PRange'], test=True))
        else:
            writer = ExcelWriter(Filepath.get_mass_results_file(
                kwargs['simYearRange'], kwargs['simMinBatRange'], 
                kwargs['NRange'], kwargs['PRange']))
        df.to_excel(writer=writer, index=False, sheet_name='Meta')
        writer.save()

    def __report_bot_results_to_excel(self, bot, writer):
        """
        bot ExcelWriter -> None
        bot: Bot | the bot for which you want to report results
        ExcelWriter: ExcelWriter | Writer object containing the path
           of the output .xlsx file

        Outputs bot info results to excel buffer. (Helper function for 
        _report_results_excel)
        """
        assert type(bot) == Bot
        assert type(writer) == _OpenpyxlWriter

        # Create series corresponding to columns of csv
        history = bot.get_history()
        player1S = Series([event[0].get_name() for event in history], 
            name='Player1')
        batAve1S = Series([event[0].get_bat_ave() for event in history], 
            name='Batting Average1')
        hit1S = Series([event[2] for event in history], name='Hit1')
        player2S = Series([event[1].get_name() for event in history], 
            name='Player2')
        batAve2S = Series([event[1].get_bat_ave() for event in history], 
            name='Batting Average2')
        hit2S = Series([event[3] for event in history], name='Hit2')
        dateS = Series([event[4] for event in history], name='Date')
        streakS = Series([event[5] for event in history], 
            name='Streak')
        otherS = Series([event[6] for event in history], 
            name='Other')

        # construct dataframe to write to excel file
        df = concat([player1S, batAve1S, hit1S, player2S, batAve2S, hit2S, 
            dateS, streakS, otherS], axis=1)

        # put df info on excel buffer
        botIndexString = str(bot.get_index())
        botLongestStreak = str(bot.get_max_streak_length())
        df.to_excel(writer, index=False,
            sheet_name='bot' + botIndexString + '-' + botLongestStreak)

    def __report_bots_metadata_results_excel(self, writer):
        """
        writer -> None
        writer: ExcelWriter | ExcelWriter object containing buffer for eventual
           output .xlsx file
        """
        assert type(writer) == _OpenpyxlWriter

        npsim = self.get_npsim()

        ## Some bookeeping
             # get percent unique bots
        percentUniqueBots = round(
            float(self.__calc_num_unique_bots()) / float(npsim.get_n()), 4)
        percentUniqueBotsString = "{0:.0f}%".format(100 * percentUniqueBots)
            # get percent mulligans used
        numMulUsed = 0
        for bot in npsim.get_bots():
            if bot.has_used_mulligan():
                numMulUsed += 1
        percentMulUsed = round(float(numMulUsed) / float(npsim.get_n()), 4)
        percentMulUsedString = "{0:.0f}%".format(100 * percentMulUsed)
            # for constructing "one item columns"
        enoughEmptyRows = ["" for i in range(npsim.get_n()-1)] 

        # Create series that correspond to columns in output excel file
        # takes advantage of the fact that self.get_bots() is in sorted order
        npsim.get_bots().sort(key=lambda bot: bot.get_max_streak_length(), 
            reverse=True)
        botS = Series([bot.get_index() for bot in npsim.get_bots()], name='Bot')
        maxStreakS = Series([bot.get_max_streak_length() for bot in \
            npsim.get_bots()], name='maxStreak')
        aveStreakS = Series([maxStreakS.mean()] + enoughEmptyRows, 
            name="aveMaxStreak")
        uniqueBotS = Series([percentUniqueBotsString] + \
            enoughEmptyRows, name='Unique Bots(%)')
        percentMulUsedS = Series([percentMulUsedString] + \
            enoughEmptyRows, name='Mul Used (%)')

        # construct dataframe to write to excel file
        df = concat(
            [botS, maxStreakS, aveStreakS, uniqueBotS, percentMulUsedS], axis=1)

        # put df info on excel buffer
        df.to_excel(writer, index=False, sheet_name='Bots Meta')

    def __report_sim_metadata_results_excel(self, writer):
        """
        writer -> None
        """
        assert type(writer) == _OpenpyxlWriter

        npsim = self.get_npsim()       

        # get number, percent of successes
        s_and_f = self.__calc_s_and_f()
        numSuccesses, percentSuccesses, numFails, percentFails = s_and_f
        percentSuccessesString = "{0:.0f}%".format(100 * percentSuccesses)
        # Find out if doubleDowns were used
        doubleDown = False
        for player2 in (event[1] for bot in npsim.get_bots() for 
            event in bot.get_history()):
            if player2 is not None:
                doubleDown = True
                break

        # construct series that correspond to columns in output file
        yearS = Series([npsim.get_sim_year()], name='simYear')
        batS = Series([npsim.get_bat_year()], name='batAveYear')
        nS = Series([npsim.get_n()], name='N')
        pS = Series([npsim.get_p()], name='P')
        startDateS = Series([npsim.get_bots()[0].get_history()[0][4]], 
            name='startDate')
        endDateS = Series([npsim.get_bots()[0].get_history()[-1][4]], 
            name='endDate')
        successS = Series([numSuccesses], name='numSuccesses')
        percentSuccessS = Series([percentSuccessesString], 
            name='percentSuccesses')
        doubleDownS = Series([doubleDown], name='DoubleDown?')

        # construct dataframe to write to excel file
        df = concat([yearS, batS, nS, pS, startDateS, endDateS, 
            successS, percentSuccessS, doubleDownS], axis=1)

        # put df info on excel buffer
        df.to_excel(writer, index=False, sheet_name='Sim Meta')

    def __calc_num_unique_bots(self):
        """
        None -> int

        Returns the number of bots in self.npsim with unique player histories
        """
        npsim = self.get_npsim()
        numUnique, N = npsim.get_n(), npsim.get_n()
        bots = npsim.get_bots()

        # if a bot is equal to any of the bots "in front of it" in the 
        # list bots, then it is not unique and we subtract 1 from numUnique
        for index, bot in enumerate(bots):
            for j in range(index+1, N):
                if bot == bots[j]:
                    numUnique -= 1
                    break

        return numUnique

    def __calc_s_and_f(self):
        """
        None -> int float int float

        Returns numSuccesses, percentSuccesses, numFailures, percentFailures
        for a completed simulation (self). 
        """
        npsim = self.get_npsim()
        # calculate num_successes
        numSuccesses = 0
        for bot in npsim.get_bots():
            if bot.get_max_streak_length() >= 57:
                numSuccesses += 1

        # Calculate other 3
        numFailures = npsim.get_n() - numSuccesses
        percentSuccesses = round(float(numSuccesses)/float(npsim.get_n()), 3)
        percentFailures = round(float(numFailures)/float(npsim.get_n()), 3)

        return numSuccesses, percentSuccesses, numFailures, percentFailures