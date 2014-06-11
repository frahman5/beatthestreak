import os
import shutil

from datetime import date

from beatthestreak.player import Player
from beatthestreak.utilities import Utilities
from beatthestreak.researcher import Researcher
from beatthestreak.retrosheet import Retrosheet
from beatthestreak.bot import Bot
from beatthestreak.filepath import Filepath

def setup():
    teardown()

def teardown():
    ## To save time, we stopped cleaning the files, since we're pretty
    ## confident that itll download if need be. We can also change this
    ## to test it again. 
    
    # get folders to clean
    # zippedFileFolder = Filepath.get_retrosheet_folder(folder='zipped')
    # unzippedFileFolder = Filepath.get_retrosheet_folder(folder='unzipped')
    testsResultsFolders = (Filepath.get_results_folder(year=year, test=True) for 
      year in range(1950, 2014))
    # for folder in (zippedFileFolder, unzippedFileFolder):
    #   os.chdir(folder)
    #   for file in os.listdir(os.getcwd()): 
    #     if os.path.isdir(file): 
    #       shutil.rmtree(file)
    #     else: 
    #       os.remove(file) 
    for folder in testsResultsFolders:
      os.chdir(folder)
      for file in os.listdir(os.getcwd()): 
        if os.path.isdir(file): 
          shutil.rmtree(file)
        else: 
          os.remove(file) 


## testPlayer variables
p1BattingAve, p2BattingAve  = 0.228, 0.287
p3BattingAve, p4BattingAve = 0.262, 0.248
p5BattingAve = 0.332 
p1 = Player(1, "Edwin", "Jackson", 2012)
p2 = Player(2, "Jose", "Reyes", 2012, debut='6/10/2003')
p3 = Player(3, "Alfonso", "Soriano", 2012)
p4 = Player(4, "Jorge", "Posada", 2010)
p5 = Player(5, "Manny", "Ramirez", 2008) # season he got traded 

## testRetrosheet variables
r2011 = Retrosheet(2011)
r2012 = Retrosheet(2012)
r2013 = Retrosheet(2013)
teamAbbrevs2013 = [('ANA','A'),('BAL','A'),('BOS','A'),('CHA','A'),
                   ('CLE','A'),('DET','A'),('HOU','A'),('KCA','A'),
                   ('MIN','A'),('NYA','A'),('OAK','A'),('SEA','A'),
                   ('TBA','A'),('TEX','A'),('TOR','A'),('ARI','N'),
                   ('ATL','N'),('CHN','N'),('CIN','N'),('COL','N'),
                   ('LAN','N'),('MIA','N'),('MIL','N'),('NYN','N'),
                   ('PHI','N'),('PIT','N'),('SDN','N'),('SFN','N'),
                   ('SLN','N'),('WAS','N')]
boxscores2013 = ("2013ANAB.txt","2013COLB.txt","2013NYNB.txt","2013TEXB.txt",   
                 "2013ARIB.txt","2013DETB.txt","2013OAKB.txt","2013TORB.txt",   
                 "2013ATLB.txt","2013HOUB.txt","2013PHIB.txt","2013WASB.txt",  
                 "2013BALB.txt","2013KCAB.txt","2013PITB.txt","2013BOSB.txt",
                 "2013LANB.txt","2013SDNB.txt","2013CHAB.txt","2013MIAB.txt",
                 "2013SEAB.txt","2013CHNB.txt","2013MILB.txt","2013SFNB.txt", 
                 "2013CINB.txt","2013MINB.txt","2013SLNB.txt","2013CLEB.txt",
                 "2013NYAB.txt","2013TBAB.txt")
eventfiles2013 = ("2013ANA.EVA","2013COL.EVN","2013NYN.EVN","2013TEX.EVA",   
                  "2013ARI.EVN","2013DET.EVA","2013OAK.EVA","2013TOR.EVA",   
                  "2013ATL.EVN","2013HOU.EVA","2013PHI.EVN","2013WAS.EVN",  
                  "2013BAL.EVA","2013KCA.EVA","2013PIT.EVN","2013BOS.EVA",
                  "2013LAN.EVN","2013SDN.EVN","2013CHA.EVA","2013MIA.EVN",
                  "2013SEA.EVA","2013CHN.EVN","2013MIL.EVN","2013SFN.EVN", 
                  "2013CIN.EVN","2013MIN.EVA","2013SLN.EVN","2013CLE.EVA",
                  "2013NYA.EVA","2013TBA.EVA")

## testBot variables
bot1 = Bot(1)
bot2 = Bot(2)


