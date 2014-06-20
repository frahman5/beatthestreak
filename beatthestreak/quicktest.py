#! pyvenv/bin/python

from cresearcher import finish_did_get_hit
from datetime import date
from filepath import Filepath

finish_did_get_hit(date=date(2012, 1, 5), 
                   firstName="Faiyam",   
                   lastName="Rahman", 
                   boxscore=Filepath.get_retrosheet_file(
                      folder='unzipped', fileF='boxscore', 
                      year=2012, team='HOU'))