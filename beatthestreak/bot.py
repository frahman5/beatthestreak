#! venv/bin/python

## Make function doc_strings include type of returned item

class Bot(object):
    """
    A robot representing an account on MLB.com for beat the streak
    Data:
        index: int[>=0] | bot number
        streak_length: int[>=0] | length of bot's  active streak
        player: Player | player that bot bets on for a given day
        player_history: List | list of all the players this bot has bet on
                               in a simulation in order from least recent
                               to most recent day
    """
    def __init__(self, index):
        self.index = index
        self.streak_length = 0
        self.player = None
        self.player_history = []
        
    def assign_player(self, player, didGetHit):
        """
        Player Bool -> None
        player: Player | the next player this bot will bet on 
        didGetHit: bool | true if player got hit on date of assignment, false otherwise
        
        Assigns a player to this bot for a given day.
        Updates player_history accordingly
        """
        self.player = player
        self.player_history.append((player, didGetHit))
        if didGetHit:
            self.incr_streak_length()
        else:
            self.reset_streak()
        
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
    
    def get_player_history(self):
        return self.player_history
    
    def get_streak_length(self):
        return self.streak_length 

    def reset_streak(self):
        self.streak_length = 0
    
