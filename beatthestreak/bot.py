import datetime

from utilities import Utilities
from player import Player

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
        Utilities.type_check(other, Bot)

        if self.get_max_streak_length() != other.get_max_streak_length():
            return False
        if self.get_history() != other.get_history():
            return False
        return True
        
    def update_history(self, player, didGetHit, date):
        """
        Player Bool date -> None
        player: Player | the next player this bot will bet on 
        didGetHit: bool | true if player got hit on date of assignment, 
            false otherwise
        date: date | date of assignment

        Assigns a player to this bot for a given day.
        Updates history accordingly
        """
        Utilities.type_check(player, Player)
        Utilities.type_check(didGetHit, bool)
        Utilities.type_check(date, datetime.date)
 
        # assign the player
        self.player = player

        # if he got a hit, increase the streak length
        if didGetHit:
            self.incr_streak_length()
        # if he didn't, update maxStreakLength if need be and reset the streak
        else:
            if self.get_streak_length() > self.get_max_streak_length():
                self.set_max_streak_length(self.get_streak_length())
            self.reset_streak()

        # update the history list
        self.history.append((player, didGetHit, date, self.streakLength))
        
    def incr_streak_length(self, amount=1):
        """
        Int -> None

        Increment this bot's streak by amount
        """
        Utilities.type_check(amount, int)

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
        Utilities.type_check(amount, int)

        self.maxStreakLength = amount

    def get_max_streak_length(self):
        return self.maxStreakLength
    
