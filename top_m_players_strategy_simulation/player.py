#! venv/bin/python 

from datetime import date
import retrosheet
from data import Data as data

class Player(object):
    """
    A player representing a MLB athlete.
    Data:
        index: int[>=0] | player index in a simulation
        id: string | retrosheet id for player
        first_name: string | Player's first name
            -> must capitalize first letter
        last_name: string | Player's last name
            -> must capitalize first letter
        bat_ave: float[0, 1] | player's batting average
    """
    
    def __init__(self, index, first_n, last_n, bat_ave):
        self.index = index
        self.first_name = first_n
        self.last_name = last_n
        self.id = self.set_retrosheet_id()
        self.bat_ave = bat_ave

    def set_retrosheet_id(self):
        """
        name: string | name of player

        Returns: string | retrosheet id of player
            If player name has multiple ids, prompts user to choose one
        """
        name = self.last_name + "," + self.first_name
        
        # Get list of possible ids
        with open(data.rootDir + data.rIdSuffix, "r") as f:
            possible_ids = [line.split(',')[2] for line in f if name in line]

        # Choose appropriate id
        if len(possible_ids) == 1:
            return possible_ids[0]
        else:
            print "Multiple ids found: "
            for id in possible_ids: print id
            print "Choose one."
            return raw_input()
        
    def get_retrosheet_id(self):
        return self.id
            
    def convert_date(self, date):
        """
        date: date(year, month, day) | a date of the year
        
        Returns: string | date in retrosheet gamelog format "yyyymmdd""
        """
        return date.isoformat().replace('-', '')

    def get_participants(self, date):
        """
        date: date(year, month, day) | a date of the year

        Returns: ListOfStrings | List of retrosheet ids corresponding to players
            starting, umps officiating, and managers managing on the given day
        """
        date = self.convert_date(date)
        with open(data.rootDir + data.gl2012Suffix, "r") as f:
            list_of_games = [line.replace('"', '').split(',')[1:]
                                    for line in f if date in line]
        return [field for game in list_of_games
                    for field in game if len(field) == 8]
    
    def did_start(self, date):
        """
        date: datetime.date(year, month, day) | a date in the year

        Returns: Boolean | True if player started a game on the given date, False otherwise
        """
        return self.get_retrosheet_id() in self.get_participants(date)

    def did_get_hit(self, date):
        """
        date: date(year, month, day) | a date in the year

        Returns: Boolean | True if player got a hit on the given date, False otherwise 
            Assumes necessary retrosheet files have been extracted (done by simulation)
        """
        # open relevant boxscore
            # find out which team he is on
                # -> need to make rosters
            # open up that teams boxscore
        # go to relevant lien in boxscore using given date
        # go to relevant line in game by using player's name
        # check the hit column. If its greater than 0, return True. Otherwise return false
        return False
    
    def get_index(self):
        return self.index
    
    def get_name(self):
        return self.first_name + " " + self.last_name
    
    def get_bat_ave(self):
        return self.bat_ave

def main():
    """
    A short test suite for Player
    """
    p1 = Player(1, "Edwin", "Jackson", 0.267)
    p2 = Player(2, "Jose", "Reyes", 0.337)

    # Test: get_retrosheet_id (simultaneously tests set_retrosheet_id)
    assert p1.get_retrosheet_id() == "jacke001"
    assert p2.get_retrosheet_id() == "reyej001"
    
    # Test: convert_date
    assert p1.convert_date(date(2012, 4, 15)) == "20120415"

    # Test: get_participants
    starting_players = ["hallt901","nelsj901","hudsm901","belld901","wedge001",
                        "melvb001","wilht001","caria001","leagb001","ackld001",
                        "hernf002","mccab001","figgc001","ackld001","suzui001",
                        "smoaj001","montj003","carpm001","olivm001","saunm001",
                        "ryanb002","weekj001","pennc001","crisc001","smits002",
                        "suzuk001","reddj001","cespy001","alleb001","sogae001"]
    assert p1.get_participants(date(2012,3,28)) == starting_players

    # Test: did_start
    assert p1.did_start(date(2012, 4, 15)) == False
    assert p2.did_start(date(2012, 4, 15)) == True

    # Test: did_get_hit
    assert p1.did_get_hit(date(2012, 5, 2)) == False
    assert p1.did_get_hit(date(2012, 6, 15)) == True

    # Test: get_index
    assert p1.get_index() == 1
    assert p2.get_index() == 2
    
    # Test: get_name
    assert p1.get_name() == "Edwin Jackson"
    assert p2.get_name() == "Jose Reyes"
    
    # Test: get_bat_ave
    assert p1.get_bat_ave() == 0.267
    assert p2.get_bat_ave() == 0.337

    print "All tests passed!"
    
if __name__ == "__main__":
    main()
