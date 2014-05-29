class Utilities(object):
    """
    A container class for commonly used generic
    utility functions
    """
    
    @classmethod
    def convert_date(self, date):
        """
        date(year, month, day) -> string
        date: date(year, month, day) | a date of the year
        
        Produces date in retrosheet gamelog format "yyyymmdd""
        """
        return date.isoformat().replace('-', '')
