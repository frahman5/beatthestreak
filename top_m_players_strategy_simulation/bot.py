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
        
    def choose_player(self, player):
        """
        Player -> None
        player: Player | the next player this bot will bet on 
        
        Assigns a player to this bot for a given day.
        Updates player_history accordingly
        """
        self.player = player
        self.player_history.append(player)
        
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

def main():
    """
    Short test suite for Bot
    """
    # When Player has been written, test choose_player, get_player and
    # get_player_history()
    
    bot1 = Bot(1)
    bot2 = Bot(2)

    # Test incr_streak_length, get_streak_length
    for i in range(4):
        bot1.incr_streak_length()
        bot2.incr_streak_length(2)
    assert bot1.get_streak_length() == 4
    assert bot2.get_streak_length() == 8

    # Test get_index
    assert bot1.get_index() == 1
    assert bot2.get_index() == 2

    print "All tests passed!"
    
if __name__ == "__main__":
    main()  
    
