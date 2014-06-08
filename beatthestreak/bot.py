import datetime

from config import specialCasesD
from utilities import Utilities
from player import Player
from exception import BotUpdateException, MulliganException
class Bot(object):
    """
    A robot representing an account on MLB.com for beat the streak
    Data:
        index: int[>=0] | bot number
        streakLength: int[>=0] | length of bot's active streak
        player: Player | player that bot bets on for a given day
        history: ListOfTuples
            Tuples = (Player, True|False, DateAssigned, StreakLengthOnDate, other)
        maxStreakLength: int[>=0] | length of bot's longest streak
        hasMulligan: bool | indicates whether or not the Bot has "mulligan", 
           or free pass if his streak would have ended length in [10,15]
        hasClaimedMulligan: bool | indicates whether or not this Bot has 
           claimed a mulligan before. Can only claim a mulligan once
    """
    def __init__(self, index):
        self.index = index
        self.streakLength = 0
        self.player = None
        self.history = []
        self.maxStreakLength = 0
        self.hasMulligan = False
        self.hasClaimedMulligan = False

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
        
    def update_history(self, player, didGetHit, date, other=None):
        """
        Player Bool date -> None
        player: Player | the next player this bot will bet on 
        didGetHit: bool OR string | true if player got hit on date of assignment, 
            false if player did not get hit on date of assignment, 'pass' if 
            player played in an invalid, suspended game on date of assigment
        date: date | date of assignment
        other: None OR string | Includes miscellaneous info on unique events
            Possible values when passed in
               1) None
               2) 'Suspended, Valid'
               3) 'Suspended, Invalid'
            Bot may also set it to any of the below
               1-3) The above 3
               4) 'Mulligan'

        Assigns a player to this bot for a given day.
        Updates history accordingly
        """
        updateHistoryOtherVals = ( None, 'Suspended, Valid', 
                                  'Suspended, Invalid')
        assert type(player) == Player
        assert (type(didGetHit) == bool) or (didGetHit == 'pass')
        assert type(date) == datetime.date
        assert other in updateHistoryOtherVals
 
        # assign the player
        self.player = player

        # if he got a hit, update streak length(& max streak length, if need be)
        if didGetHit == True:
            self.incr_streak_length()
            if self.get_streak_length() > self.get_max_streak_length():
                self.set_max_streak_length(self.get_streak_length())
        # if he didn't...
        elif didGetHit == False:
            # and its mulligan time: leave streak, update other, kill mulligan
            if (self.get_mulligan_status() and \
                self.get_streak_length() in (10, 11, 12, 13, 14, 15)):
                other = specialCasesD['M']
                self.hasMulligan = False
            # otherwise reset the streak
            else:
                self.reset_streak()
        # if this bot is getting a pass, leave the streak alone
        elif didGetHit == 'pass':
            pass 
        # if none of the above occured, we have a problem
        else:  # pragma: no cover
            raise BotUpdateException("Update with player {0}".format(player) + \
                ", didGetHit: {0}, date: {1}".format(didGetHit, date) + \
                ", other: {0} was invalid".format(other))

        # update the history list
        self.history.append((player, didGetHit, date, self.streakLength, other))
        
    def incr_streak_length(self, amount=1):
        """
        Int -> None

        Increment this bot's streak by amount
        """
        assert type(amount) == int

        self.streakLength += amount
        
    def get_index(self):
        return self.index
    
    def get_player(self):
        return self.player
    
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
