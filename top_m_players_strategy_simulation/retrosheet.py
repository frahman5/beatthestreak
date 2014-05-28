#! venv/bin/python 

import urllib
import os
import zipfile
import subprocess

from data import Data as data

class Retrosheet(object):
    """
    A Retrosheet API to download event files and parse them
    for relevant boxscores

    Data:
        Season: String | Indicates which season's event files this
            object handles (format: yyyy)
        destZipped: String | Indicates where zipped event files go
        destUnzipped: String | Indicates where unzipped event
            files go
        eventFileZipped: String | Path of zipped event file
        eventFileUnzipped: String | Path of directory of unzipped event files
    """
    def __init__(self, season, destZipped=data.rootDir + data.defaultDestZippedSuffix, 
                    destUnzipped=data.rootDir + data.defaultDestUnzippedSuffix):
        self.season = str(season)
        self.destZipped = destZipped
        self.destUnzipped = destUnzipped
        self.eventFileZipped = self.destZipped + "/r" + self.season + "events.zip"
        self.eventFileUnzipped = self.destUnzipped + "/events" + self.season

    def download(self, type='playByPlay'):
        """
        downloads retrosheet event files for self.season of type type

        type: String | Indicates which type of event file to download 
            (gamelog, play by play, etc)
        """
        
        if os.path.isfile(self.eventFileZipped):
            return
        if type == 'playByPlay':
            url = 'http://www.retrosheet.org/events/' + self.season + "eve.zip"
            urllib.urlretrieve(url, filename=self.eventFileZipped)

    def unzip(self, type='playByPlay'):
        """
        unzips retrosheet event files for self.season of type type

        type: String | Indicates which type of event file to unzip
            (gamelog, play by play, etc)
        """
        if not os.path.isfile(self.eventFileZipped):
            self.download()

        zf = zipfile.ZipFile(self.eventFileZipped)
        zf.extractall(path=self.eventFileUnzipped)

    def gen_boxscores(self):
        """
        Generates boxscores for each team in season self.season.
        Requires that play-by-play event files have been unzipped to 
            self.destUnzipped
        Stores boxscores in .txt files in self.destUnzipped
        """
        teamAbbrevs = self.gen_team_abbrevs()
        callPrefix = ['cwbox', '-a', '-y', self.season]

        os.chdir(self.destUnzipped + "/events" + self.season)
        for team in teamAbbrevs:
            call = callPrefix + [self.season + team[0] + ".EV" + team[1]]
            print "team: %s, call: %s" % (team, call)
            with open(self.season + team[0] + "B" + ".txt", "w+") as file:
                subprocess.call(call, stdout=file)

    def gen_team_abbrevs(self):
        """
        Extracts 3 letter abbreviations and league
        affiliation for all MLB teams in season self.season
        from file teamyyyy where yyyy = self.season

        Requires and assumes that play-by-play event files have been 
            unzipped to self.destUnzipped
        """
        #cwbox only works if team is lowercase
        defaultTeamPath = self.eventFileUnzipped + "/TEAM" + self.season
        functionalTeamPath = self.eventFileUnzipped + "/team" + self.season
        if os.path.isfile(defaultTeamPath):
            os.rename(defaultTeamPath, functionalTeamPath)

        with open(functionalTeamPath, "r") as f:
            teamAbbrevs = [(line.split(',')[0], line.split(',')[1]) for
                                line in f]
        return teamAbbrevs

    def clean_used_files(self):
        """
        Removes all zipped retrosheet files, as well as used event files

        To be used after necessary information has been extracted and parsed
        """
        os.chdir(self.destUnzipped + "/events" + self.season)
        [os.remove(file) for file in os.listdir(os.getcwd()) 
            if file.endswith(".EVA") or file.endswith(".EVN") or 
            file.endswith("team" + self.season)]

        os.chdir(self.destZipped)
        [os.remove(file) for file in os.listdir(os.getcwd()) 
            if file.endswith(".zip")]

    def get_season(self):
        return self.season

    def get_dest_zipped(self):
        return self.destZipped

    def get_dest_unzipped(self):
        return self.destUnzipped

    def get_event_file_zipped(self):
        return self.eventFileZipped

    def get_event_file_unzipped(self):
        return self.eventFileUnzipped


def main():
    """
    Short test Suite for Retrosheet
    """
    ## To Test: Data getters and setters

    r2013 = Retrosheet(2013)

    #################### Test: download ####################
    r2013.download()
    assert os.path.isfile(r2013.get_event_file_zipped())

    #################### Test: unzip ####################
    r2013.unzip()
    assert os.path.isfile(r2013.get_event_file_unzipped() + "/2013ANA.EVA")
    assert os.path.isfile(r2013.get_event_file_unzipped() + "/2013OAK.EVA")

    #################### Test: gen_team_abbrevs ####################
    teamAbbrevs2013 = [('ANA','A'),('BAL','A'),('BOS','A'),('CHA','A'),
                       ('CLE','A'),('DET','A'),('HOU','A'),('KCA','A'),
                       ('MIN','A'),('NYA','A'),('OAK','A'),('SEA','A'),
                       ('TBA','A'),('TEX','A'),('TOR','A'),('ARI','N'),
                       ('ATL','N'),('CHN','N'),('CIN','N'),('COL','N'),
                       ('LAN','N'),('MIA','N'),('MIL','N'),('NYN','N'),
                       ('PHI','N'),('PIT','N'),('SDN','N'),('SFN','N'),
                       ('SLN','N'),('WAS','N')]
    assert r2013.gen_team_abbrevs() == teamAbbrevs2013

    #################### Test: gen_boxscores ####################
    r2013.gen_boxscores()
    boxscores2013 = ("2013ANAB.txt","2013COLB.txt","2013NYNB.txt","2013TEXB.txt",   
                     "2013ARIB.txt","2013DETB.txt","2013OAKB.txt","2013TORB.txt",   
                     "2013ATLB.txt","2013HOUB.txt","2013PHIB.txt","2013WASB.txt",  
                     "2013BALB.txt","2013KCAB.txt","2013PITB.txt","2013BOSB.txt",
                     "2013LANB.txt","2013SDNB.txt","2013CHAB.txt","2013MIAB.txt",
                     "2013SEAB.txt","2013CHNB.txt","2013MILB.txt","2013SFNB.txt", 
                     "2013CINB.txt","2013MINB.txt","2013SLNB.txt","2013CLEB.txt",
                     "2013NYAB.txt","2013TBAB.txt")
    for path in boxscores2013:
        assert os.path.isfile(r2013.get_dest_unzipped() + "/events2013/" + path)

    #################### Test: gen_rosters ####################
    r2013.gen_rosters()
    rosters2013 = ("2013ANAR.txt","2013COLR.txt","2013NYNR.txt","2013TEXR.txt",   
                   "2013ARIR.txt","2013DETR.txt","2013OAKR.txt","2013TORR.txt",   
                   "2013ATLR.txt","2013HOUR.txt","2013PHIR.txt","2013WASR.txt",  
                   "2013BALR.txt","2013KCAR.txt","2013PITR.txt","2013BOSR.txt",
                   "2013LANR.txt","2013SDNR.txt","2013CHAR.txt","2013MIAR.txt",
                   "2013SEAR.txt","2013CHNR.txt","2013MILR.txt","2013SFNR.txt", 
                   "2013CINR.txt","2013MINR.txt","2013SLNR.txt","2013CLER.txt",
                   "2013NYAR.txt","2013TBAR.txt")
    for path in boxscores2013:
        assert os.path.isfile(r2013.get_dest_unzipped() + "/events2013/" + path)

    #################### Test: clean_used_files ####################
    eventfiles2013 = ("2013ANA.EVA","2013COL.EVN","2013NYN.EVN","2013TEX.EVA",   
                      "2013ARI.EVN","2013DET.EVA","2013OAK.EVA","2013TOR.EVA",   
                      "2013ATL.EVN","2013HOU.EVA","2013PHI.EVN","2013WAS.EVN",  
                      "2013BAL.EVA","2013KCA.EVA","2013PIT.EVN","2013BOS.EVA",
                      "2013LAN.EVN","2013SDN.EVN","2013CHA.EVA","2013MIA.EVN",
                      "2013SEA.EVA","2013CHN.EVN","2013MIL.EVN","2013SFN.EVN", 
                      "2013CIN.EVN","2013MIN.EVA","2013SLN.EVN","2013CLE.EVA",
                      "2013NYA.EVA","2013TBA.EVA")
    for path in eventfiles2013:
        assert os.path.isfile(r2013.get_dest_unzipped() + "/events2013/" + path)
    r2013.clean_used_files()
    for path in eventfiles2013:
        assert not os.path.isfile(r2013.get_dest_unzipped() + "/events2013/" + path)

    print "All tests passed!"

if __name__ == "__main__":
    main()
