import datetime
from retrosheet import Retrosheet
from utilities import Utilities
from researcher import Researcher
from exception import DifficultYearException

class Simulation(object):
    """
    A simulation of a beat the streak strategy over a given
    number of days
    Data:
        Year: MLB Season (YYYY) in which to run the simulation
        startDate: string|date | default indicates opening day, otherwise
           indicate a startDate
    """
    def __init__(self, year, startDate='default'):
    	"""
    	int string|date -> None
        simYear: 4 digit int indicating in which season to run the simulation
        currentDate: date | startDate for simulation
        """
        #assert type(year) == int
        #assert (type(startDate) == str) or (type(startDate) == datetime.date)

        self.simYear = self._check_year(year)
        if startDate == 'default':
            self.currentDate = Researcher.get_opening_day(year)
        else:
            #assert type(startDate) == datetime.date
            Researcher.check_date(startDate, startDate.year)
            self.currentDate = startDate

    def _check_year(self, year):
        """
        int -> None|int
        Produces an exception if year is before 1962 or a strike year (1972, 
            1982, 1994, 1995) since 1962. Returns the given year otherwise.
        """
        #assert type(year) == int

        # Since 1962 the season has been 162 games and 3.1 PAs per game, or 502
        # per season has been the min requirement for batting title contention.
        # This figure is altered for the strikeYears and years before 1962.
        if (year <= 1962) or (year in (1972, 1981, 1994, 1995)):
            raise DifficultYearException("The years 1972, 1981, 1994, 1995 " + \
                "had strikes, and the years before 1962 didn't have 162 games." + \
                " Please simulate in another year") 
        else:
            return year

    def setup(self):
    	"""
    	None -> None

    	Downloads and parses necessary retrosheet data for the simulation
    	"""
        retro = Retrosheet(self.simYear)
        Utilities.ensure_gamelog_files_exist(self.simYear)
        Utilities.ensure_boxscore_files_exist(self.simYear, 'HOU')
        retro.clean_used_files()

    def close(self):
    	"""
    	None -> None

    	Deletes residual files from the simulation
    	"""
    	Utilities.clean_retrosheet_files()

    def set_sim_year(self, year):
        self.simYear = year

    def get_sim_year(self):
        return self.simYear

    def set_date(self, date):
        #assert type(date) == datetime.date
        self.currentDate = date
    
    def get_date(self):
        return self.currentDate