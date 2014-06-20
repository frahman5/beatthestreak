#! pyvenv/bin/python

from cresearcher import finish_did_get_hit
from researcher import Researcher as R
from datetime import date
from filepath import Filepath
from player import Player

Jose = Player("Jose", "Reyes", 2012, debut='6/10/2003')

R.did_get_hit(date(2012, 6, 16), Jose) # name in first half of boxscore line
R.did_get_hit(date(2012, 6, 5), Jose)  # name in second half of boxscore line
# finish_did_get_hit(date=date(2012, 6, 16), 
#                    firstName="Faiyam",   
#                    lastName="Rahman", 
#                    boxscore=Filepath.get_retrosheet_file(
#                       folder='unzipped', fileF='boxscore', 
#                       year=2012, team='TBA'))