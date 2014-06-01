#! venv/bin/python

## Make function doc_strings include type of returned item

class Bot(object):
    """
    A robot representing an account on MLB.com for beat the streak
    Data:
        index: int[>=0] | bot number
        streak_length: int[>=0] | length of bot's  active streak
        player: Player | player that bot bets on for a given day
        history: ListOfTuples
            Tuples = (Player, True|False, DateAssigned, StreakLength)
    """
    def __init__(self, index):
        self.index = index
        self.streak_length = 0
        self.player = None
        self.history = []
        self.max_streak_length = 0
        
    def assign_player(self, player, didGetHit, date):
        """
        Player Bool date -> None
        player: Player | the next player this bot will bet on 
        didGetHit: bool | true if player got hit on date of assignment, false otherwise
        date: date of assignment

        Assigns a player to this bot for a given day.
        Updates history accordingly
        """
        self.player = player
        if didGetHit:
            self.incr_streak_length()
        else:
            if self.streak_length > self.max_streak_length:
                self.max_streak_length = self.streak_length
            self.reset_streak()
        self.history.append((player, didGetHit, date, self.streak_length))
        
    def incr_streak_length(self, amount=1):
        """
        Int -> None

        Increment this bot's streak by amount
        """
        self.streak_length += amount
        
    def get_index(self):
        return self.index
    
    def get_player(self):
        return self.player
    
    def get_history(self):
        return self.history
    
    def get_streak_length(self):
        return self.streak_length 

    def reset_streak(self):
        self.streak_length = 0

    def get_max_streak_length(self):
        return self.max_streak_length
    
