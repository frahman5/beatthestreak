import os
import pandas as pd

from datetime import date, datetime

from utilities import Utilities
from retrosheet import Retrosheet
from exception import NoPlayerException
from researcher import Researcher
from filepath import Filepath

class Player(object):
    """
    An MLB athlete.
    Attributes:
        rId: string | player's retrosheet id
        lId: string | player's lahman id
        firstName: string | Player's first name
            -> Capitalized First Letter
        lastName: string | Player's last name
            -> Capitalized First letter
        batAve: float[0, 1] | player's batting average
        debut: string(mm/dd/yyyy) | date of player's debut
    """ 
    # @profile
    def __init__(self, *args, **kwargs):
        """
        Can construct in multiple ways:
        1) Player(lahmanID, batAveYear)
            -> takes lahmanID and batAveYear. Obtains name, retrosheetID and
            batting average on its own
        1a) Player(lahmanID, batAveYear, batAve=INT, firstName=firstName,  
                   lastName=lastName, retrosheetID=retrosheetID)
            -> takes lahmanId, batAveYear, batAve, firstName, lastName. Obtains
               retrosheetID on its own. PREDOMINANT INIT USED IN SIMULATIONS
        2) Player(firstN, lastN, batAveYear)
            -> constructor will find retrosheet id, lahman id, batting ave, and
            if necessary prompt the user for a debut date
        3) Player(firstN, lastN, batAveYear, debut='mm/dd/yyyy')
            -> same as above, except now with player debut date specified, 
            there is no chance of ambiguity in retrieving a retrosheet id
            -> if debut was september 4th, 1990, do debut='9/4/1990'
        """
        # Type 1, 1a construction
        if len(args) == 2: 
            assert type(args[0]) == str # lahman ID
            assert type(args[1]) == int # batAveYear
            self.lId = args[0]
            ## Check if its type 1a
            if 'batAve' in kwargs.keys():
                assert 'firstName' in kwargs.keys()
                assert 'lastName' in kwargs.keys()
                assert 'retrosheetID' in kwargs.keys()
                self.batAve = kwargs['batAve']
                self.firstName = kwargs['firstName']
                self.lastName = kwargs['lastName']
                self.rId = kwargs['retrosheetID']
            else: 
                self.firstName, self.lastName = Researcher.name_from_lahman_id(self.lId)
                self.batAve = self._set_bat_ave(args[1])
                self.rId = self.__set_retrosheet_id(source='lahmanID')
            self.debut = None
            return

        # else Types 2 and 3 construction
        assert len(args) == 3
        assert type(args[0]) == str # first name
        assert type(args[1]) == str # last name
        assert type(args[2]) == int # batAveYear

        if 'debut' in kwargs.keys():
            self.debut = kwargs['debut']
        else:
            self.debut = None

        self.firstName = args[0]
        self.lastName = args[1]
        self.rId = self.__set_retrosheet_id(source='name')
        self.lId = self.__set_lahman_id()
        self.batAve = self._set_bat_ave(args[2])

    def __eq__(self, other):
        # technically, only need one. but dependability via redundancy :)
        samerId = (self.get_retrosheet_id() == other.get_retrosheet_id())
        samelId = (self.get_lahman_id() == other.get_lahman_id())
        return samerId and samelId

    def __str__(self):
        return self.get_name() + ": %.3f" % self.get_bat_ave()

    def __repr__(self):
        return self.__str__()


    def __set_retrosheet_id(self, source='name'):
        """
        int -> string
        source: string | Indicates whether self should use a name or a lahmanID
            to find the retrosheet id. Must be in ('name', 'lahmanID')

        Returns retrosheet id of self
        """
        assert type(source) == str
        assert source in ('name', 'lahmanID')

        if source == 'name':
            return self.fetch_retrosheet_id_from_name()
        if source == 'lahmanID':
            return self.fetch_retrosheet_id_from_lahman_ID()

    def fetch_retrosheet_id_from_name(self):
        """
        None -> string

        Produces retrosheet id of self from self.firstName and self.LastName 
        and potentially self.debut
        """
        # open retrosheet id file and get rows corresponding to name
        df = pd.read_csv(Filepath.get_retrosheet_file(
            folder='base', fileF='id'))
        df = df[df.FIRST == self.get_first_name()]
        df = df[df.LAST == self.get_last_name()]

        if len(df) == 0: # if no rows found, raise an exception
            raise NoPlayerException("No player found with name %s" % \
                    self.get_first_name()+ " " + self.get_last_name())
        if len(df) == 1: # if 1 row found, unique player found. return id
            return df.ID.item()

        # else len(df) > 1. If debut date given, find corresponding id. 
        # Otherwise, prompt user for debut date and find id
        i = 0
        while self.get_debut() not in df.DEBUT.values:
            if i > 0: print "\nYou mistyped. Try again"
            print "\nMultiple ids found. What was " + \
                "%s's debut date? Options:" % self.get_name()
            for debut in df.DEBUT: print debut
            self.set_debut(str(raw_input()))
            i += 1

        for debut in df.DEBUT: # find right debut date and return id
            if datetime.strptime(debut, '%m/%d/%Y') == \
                 datetime.strptime(self.debut, '%m/%d/%Y'):
                return df[df.DEBUT == debut].ID.item()

    def fetch_retrosheet_id_from_lahman_ID(self):
        """
        None -> string

        Produces retrosheet id of self from self.lId
        """
        # open lahman master.csv, get right row and return id
        df = pd.read_csv(Filepath.get_lahman_file("master"), 
                usecols=['playerID', 'retroID'])
        return df[df.playerID == self.lId].retroID.item()

    def __set_lahman_id(self):
        # get lahman master csv with playerID and retroID rows
        df = pd.read_csv(Filepath.get_lahman_file("master"), 
                         usecols=["playerID", "retroID"])
        
        # Get lahmanId corresponding to self's retrosheet id
        return df[df.retroID == self.get_retrosheet_id()]['playerID'].item()
        
    def get_retrosheet_id(self):
        return self.rId

    def get_name(self):
        return self.firstName + " " + self.lastName

    def get_last_name(self):
        return self.lastName

    def get_first_name(self):
        return self.firstName

    def get_debut(self):
        return self.debut

    def set_debut(self, debut):
        assert type(debut) == str

        self.debut = debut

    def get_bat_ave(self):
        return self.batAve

    def get_lahman_id(self):
        return self.lId

    def _set_bat_ave(self, year):
        """
        int -> float
        year: int | year as a 4 digit int

        Produces the season batting average of self in year year, rounded
        off to 3 decimal places
        """
        assert type(year) == int

        # Read in relevant columns from batting.csv
        df = pd.read_csv(Filepath.get_lahman_file("batting"), 
                         usecols=['playerID', 'yearID', 'AB', 'H'])

        # Getting batting stats for player in given year
        lId = self.get_lahman_id()
        batting_stats_df = df[df.playerID == lId][df.yearID == year]

        # Sum over all the hits and divide by the sum over all at-bats
        #   accounts for players who were traded mid season via summing
        return round(sum(batting_stats_df.H) / sum(batting_stats_df.AB), 3)