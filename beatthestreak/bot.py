import datetime

from utilities import Utilities
from player import Player
from exception import BotUpdateException
class Bot(object):
    """
    A robot representing an account on MLB.com for beat the streak
    Data:
        index: int[>=0] | bot number
        streakLength: int[>=0] | length of bot's active streak
        player: Player | player that bot bets on for a given day
        history: ListOfTuples
            Tuples = (Player, True|False, DateAssigned, StreakLengthOnDate)
        maxStreakLength: int[>=0] | length of bot's longest streak
    """
    def __init__(self, index):
        self.index = index
        self.streakLength = 0
        self.player = None
        self.history = []
        self.maxStreakLength = 0

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
        
    def update_history(self, player, didGetHit, date):
        """
        Player Bool date -> None
        player: Player | the next player this bot will bet on 
        didGetHit: bool OR string | true if player got hit on date of assignment, 
            false if player did not get hit on date of assignment, 'pass' if 
            player played in an invalid, suspended game on date of assigment
        date: date | date of assignment

        Assigns a player to this bot for a given day.
        Updates history accordingly
        """
        assert type(player) == Player
        assert (type(didGetHit) == bool) or (didGetHit == 'pass')
        assert type(date) == datetime.date
 
        # assign the player
        self.player = player

        # if he got a hit, increase the streak length
        if didGetHit == True:
            self.incr_streak_length()

        # if he didn't, update maxStreakLength if need be and reset the streak
        elif didGetHit == False:
            if self.get_streak_length() > self.get_max_streak_length():
                self.set_max_streak_length(self.get_streak_length())
            self.reset_streak()

        # if this bot is getting a pass, leave the streak alone
        elif didGetHit == 'pass':
            pass 

        # if none of the above occured, we have a problem
        else:  # pragma: no cover
            raise BotUpdateException("Update with player {0}".format(player) + \
                ", didGetHit: {0}, date: {1}".format(didGetHit, date) + \
                " was invalid")

        # update the history list
        self.history.append((player, didGetHit, date, self.streakLength))
        
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
    
