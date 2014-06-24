import datetime

from config import specialCasesD
from utilities import Utilities
from player import Player
from exception import BotUpdateException, MulliganException
from researcher import Researcher

class Bot(object):
    """
    A robot representing an account on MLB.com for beat the streak
    Data:
        index: int[>=0] | bot number
        streakLength: int[>=0] | length of bot's active streak
        players: TupleOfPlayers | If bot is playing a double down, will be a 
           tuple of length 2. Otherwise, a tuple of length 1
        history: ListOfTuples
            Tuples = (Player1, Player2, Player1HitVal, Player2HitVal, DateAssigned, StreakLengthOnDate, other)
        maxStreakLength: int[>=0] | length of bot's longest streak
        hasMulligan: bool | indicates whether or not the Bot has "mulligan", 
           or free pass if his streak would have ended length in [10,15]
        hasClaimedMulligan: bool | indicates whether or not this Bot has 
           claimed a mulligan before. Can only claim a mulligan once
        lastHistory: Tuple | same structure as a history tuple. Holds the
           last entered History item, for speedups
    """
    def __init__(self, index):
        self.index = index
        self.streakLength = 0
        self.players = None
        self.history = []
        self.maxStreakLength = 0
        self.hasMulligan = False
        self.hasClaimedMulligan = False
        self.lastHistory = ()

    def __eq__(self, other):
        """
        Bots are considered equal if they have the same maxStreakLength
        and identical player histories
        """
        assert type(other) == Bot

        if self.get_max_streak_length() != other.get_max_streak_length():
            return False
        if self.get_history() != other.get_history():
            return False
        return True

    # @profile
    def update_history(self, p1=None, p2=None, date=None, susGamesDict=None, 
           bot=None):
        """
        Player Player(optional) date dict -> None
            p1 : Player | player to assign to bot in case of single or double Down
            p2 : Player | OPTIONAL : 2nd player to assign, in case of double Down
            date : datetime.date | date of assignment of players
            susGamesDict : dict | dictionary of suspended games as defined in 
                Researcher.
            bot: Bot | OPTIONAL. A bot from which to copy the last history item. 

        Updates history in one of three ways:
            1) Given bot: copies the given bot's last history tuple
            2) Given p1, p2, date, susGamesDict: updates history as a double down
            3) Given p1, date, susGamesDict: updates history as a single down 
        """
        # type checking done in helper functions

        if bot: # update type 1
            for param in (p1, p2, date, susGamesDict):
                assert param is None
            self.__update_history_from_bot(bot)
        elif p2: # update type 2
            assert bot is None
            self.__update_history_double_down(p1, p2, date, susGamesDict)
        elif not p2: # update type 3
            assert bot is None
            self.__update_history_single_down(p1, date, susGamesDict)

    # @profile
    def __update_history_from_bot(self, otherBot): 
        """
        bot -> None

        Copies all but the streakLength item from otherBot's last history, 
        Updates assigned players
        Updates streak length 
        Updates last_history
        """
        otherHistory = otherBot.get_last_history()

        p1, p2, hitVal1, hitVal2 = otherHistory[0:4]
        date = otherHistory[4]
        otherInfo = otherHistory[6]

        # update players (same for single and downDown)
        self.players = p1, p2

        ## Update streakLength, maxStreakLength, and otherInfo if needbe
        ## Is it a single down?
        if None in (hitVal1, hitVal2):
            hitVal = [hitVal for hitVal in (hitVal1, hitVal2) 
                      if hitVal is not None][0]
            # Case 1: Player got a hit
            if hitVal == True:
                self.incr_streak_length()
            # Case 2: No Hit
            elif hitVal == False: 
                # Case 2.1: Mulligan time
                if (self.get_mulligan_status() and \
                    self.get_streak_length() in (10, 11, 12, 13, 14, 15)):
                    if otherInfo:
                        otherInfo = otherInfo + ' ' + specialCasesD['M']
                    else:
                        otherInfo = specialCasesD['M']
                    self.hasMulligan = False 
                # Case 2.2: Not Mulligan Time
                else:
                    self.reset_streak()
            # Case 3: Pass
            elif hitVal == 'pass':
                pass
            # Case 4: None of the above, houston we have a problem!!
            else: # pragma: no cover
                raise BotUpdateException("Copy Update from bot with history" + \
                "{} failed".format(otherHistory))
        else: ## else handle the doubledown cases
            mulliganUsed = False # local indicator of mulligan use
                 # get unordered collection of hitVals
            hitVals = set([hitVal1, hitVal2]) 
                 # Case 1: Two hits
            if hitVals == set([True, True]): 
                self.incr_streak_length(amount=2)
                 # Case 2: Two passes
            elif hitVals == set(['pass', 'pass']):
                pass
                 # Case 3 : One hit, one pass
            elif hitVals == set([True, 'pass']): 
                self.incr_streak_length(amount=1)
                 # Case 4: One no hit + one of (Hit, No hit, Pass)
            elif False in hitVals:
                    # Case 4.1: Mulligan time
                if (self.get_mulligan_status() and \
                    self.get_streak_length() in (10, 11, 12, 13, 14, 15)):
                    self.hasMulligan = False
                    mulliganUsed = True 
                    # Case 4.2: Not Mulligan time
                else:
                    self.reset_streak()
                # Case 5: None of the above--houston we have a problem!
            else: # pragma: no cover
                raise BotUpdateException("Copy Update from bot with history" + \
                    "{} failed".format(otherHistory))
            # finalize otherInfo 
            if otherInfo and mulliganUsed:
                otherInfo = otherInfo + ' ' + specialCasesD['M']

        # update history tuple and lastHistory
        self.set_last_history((p1, p2, hitVal1, hitVal2, 
                             date, self.get_streak_length(), otherInfo))

    # @profile
    def __update_history_double_down(self, p1, p2, date, susGamesDict):
        """
        Player Player date dict -> None
            p1 : Player | player to assign to bot
            p2 : Player | second player to assign to bot
            date : date on which to assign player
            susGamesDict: dictionary of suspended games as defined in Researcher

        Updates bot history with a double_down play on date date for players
        p1 and p2. Updates streakLength, maxStreakLength (if need be), and includes
        "other" column in history if need be
        """
        assert type(p1) == Player
        assert type(p2) == Player
        assert type(date) == datetime.date
        assert type(susGamesDict) == dict

        otherInfoVals = (None, specialCasesD['S']['V'], 
                         specialCasesD['S']['I'], specialCasesD['M'], 
                         specialCasesD['SA'])
        mulliganUsed = False # mulligan use indicator, for otherInfo concat

        # update assigned players and get their hit information
        self.players = (p1, p2)
        hitVal1, otherInfo1 = Researcher.get_hit_info(date, p1, susGamesDict)
        hitVal2, otherInfo2 = Researcher.get_hit_info(date, p2, susGamesDict)
        assert otherInfo1 in otherInfoVals
        assert otherInfo2 in otherInfoVals

        # get unordered collection of hitVals
        hitVals = set([hitVal1, hitVal2]) 

        ## Update streak length and max streak length
        # Case 1: Two hits
        if hitVals == set([True, True]): 
            self.incr_streak_length(amount=2)
        # Case 2: Two passes
        elif hitVals == set(['pass', 'pass']):
            pass
        # Case 3 : One hit, one pass
        elif hitVals == set([True, 'pass']): 
            self.incr_streak_length(amount=1)
        # Case 4: One no hit + one of (Hit, No hit, Pass)
        elif False in hitVals:
            # Case 4.1: Mulligan time
            if (self.get_mulligan_status() and \
                self.get_streak_length() in (10, 11, 12, 13, 14, 15)):
                self.hasMulligan = False
                mulliganUsed = True # local indicator of mulligan use
            # Case 4.2: Not Mulligan time
            else:
                self.reset_streak()
        # Case 5: None of the above--houston we have a problem!
        else: # pragma: no cover
            raise BotUpdateException("Update with players {0} {1}".format(p1, p2) + \
                ", hitVals: {0} {1}, date: {2}".format(hitVal1, hitVal2, date) + \
                ", other: {0} {1} was invalid".format(otherInfo1, otherInfo2))

        # finalize otherInfo 
        otherInfo = self.__concat_other_infos(
            otherInfo1, otherInfo2,mulligan=mulliganUsed)

        # update history list
        hist = (p1, p2, hitVal1, hitVal2, date, 
                            self.get_streak_length(), otherInfo)
        self.set_last_history(hist)
        
    def __update_history_single_down(self, p1, date, susGamesDict):
        """
        Player date dict -> None
            p1 : Player | player to assign to bot
            date : date on which to assign player
            susGamesDict: dictionary of suspended games as defined in Researcher

        Updates bot history with a single_down player on date date for player
        p1. Updates streakLength, maxStreakLength (if need be), and includes
        "other" column in history if need be
        """
        assert type(p1) == Player
        assert type(date) == datetime.date
        assert type(susGamesDict) == dict

        otherInfoVals = (None, specialCasesD['S']['V'], 
                         specialCasesD['S']['I'], specialCasesD['M'], 
                         specialCasesD['SA'])

        # update assigned player and get his hit information
        self.players = (p1, None)
        hitVal, otherInfo = Researcher.get_hit_info(date, p1, susGamesDict)
        assert otherInfo in otherInfoVals

        ## Update streak length and max streak length
        # Case 1: Player got a hit
        if hitVal == True:
            self.incr_streak_length()
        # Case 2: No Hit
        elif hitVal == False: 
            # Case 2.1: Mulligan time
            if (self.get_mulligan_status() and \
                self.get_streak_length() in (10, 11, 12, 13, 14, 15)):
                if otherInfo:
                    otherInfo = otherInfo + ' ' + specialCasesD['M']
                else:
                    otherInfo = specialCasesD['M']
                self.hasMulligan = False 
            # Case 2.2: Not Mulligan Time
            else:
                self.reset_streak()
        # Case 3: Pass
        elif hitVal == 'pass':
            pass
        # Case 4: None of the above, houston we have a problem!!
        else: # pragma: no cover
            raise BotUpdateException("Update with player {0}".format(player) + \
                ", didGetHit: {0}, date: {1}".format(didGetHit, date) + \
                ", other: {0} was invalid".format(other))

        # update history list
        hist = (p1, None, hitVal, None, date, 
                            self.get_streak_length(), otherInfo)
        self.set_last_history(hist)

    def __concat_other_infos(self, otherInfo1, otherInfo2, mulligan=False):
        """
        None|String None|String bool -> string|None
            otherInfo1: string | otherInfo from R.get_hit_info()
            otherInfo2: string | otherInfo from R.get_hit_info()
            mulligan: bool | indicates whether a mulligan has been has_used_mulligan

        Produces a otherInfo string or None to be used in the outcome of a 
        update_history function call
        """
        assert (not otherInfo1) or (type(otherInfo1) == str)
        assert (not otherInfo2) or (type(otherInfo2) == str)
        assert type(mulligan) == bool

        # Concatenate otherInfos
        if (not otherInfo1) and (not otherInfo2): # both None
            otherInfo = None
        if otherInfo1 and not otherInfo2: # otherInfo2 None
            otherInfo = otherInfo1
        if not otherInfo1 and otherInfo2: # otherInfo1 None
            otherInfo = otherInfo2
        if otherInfo1 and otherInfo2: # both not None
            otherInfo = otherInfo1 + ' ' + otherInfo2

        # Update otherInfo if mulligan was used
        if mulligan and otherInfo:
            otherInfo = otherInfo + ' ' + specialCasesD['M']
        elif mulligan and not otherInfo:
            otherInfo = specialCasesD['M']

        return otherInfo

    def incr_streak_length(self, amount=1):
        """
        Int -> None

        Increment this bot's streak by amount and update max streak length
        if need be
        """
        assert type(amount) == int

        self.streakLength += amount

        if self.streakLength > self.get_max_streak_length():
            self.set_max_streak_length(self.streakLength)
        
    def get_index(self):
        return self.index
    
    def get_players(self):
        return self.players
    
    def get_history(self):
        return self.history
    
    def get_streak_length(self):
        return self.streakLength 

    def reset_streak(self):
        self.streakLength = 0

    def set_max_streak_length(self, amount):
        assert type(amount) == int

        self.maxStreakLength = amount

    def get_max_streak_length(self):
        return self.maxStreakLength
    
    def get_mulligan_status(self):
        return self.hasMulligan

    def has_used_mulligan(self):
        return self.hasClaimedMulligan and (not self.hasMulligan)
        
    def claim_mulligan(self):
        if not self.hasClaimedMulligan:
            self.hasMulligan = True
            self.hasClaimedMulligan = True
        else:
            raise MulliganException("Bot {0} has ".format(self.get_index()) + \
                "its mulligan. Can only claim one mulligan per bot!")

    def get_last_history(self):
        return self.lastHistory

    def set_last_history(self, history):
        """
        Updates the lastHistory Buffer and puts the tuple in
        self.history as well
        """
        assert type(history) == tuple
        assert len(history) == 7

        self.lastHistory = history
        self.history.append(history)
