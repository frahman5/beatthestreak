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
        self.eventFileZipped = self.destZipped + "/r" + self.season + \
                                 "events.zip"
        self.eventFileUnzipped = self.destUnzipped + "/events" + self.season
        self.gamelogFileZipped = self.destZipped + "/rGamelog" + \
                                  self.season + ".zip"
        self.gamelogFileUnzipped = self.destUnzipped + "gamelog"

    def download(self, type='event'):
        """
        downloads retrosheet files for self.season of type type

        type: String | Indicates which type of event file to download 
            (gamelog, event, id)
        """
        if type == 'event':
            if os.path.isfile(self.eventFileZipped): return
            url = 'http://www.retrosheet.org/events/' + self.season + "eve.zip"
            urllib.urlretrieve(url, filename=self.eventFileZipped)
        if type == 'gamelog':
            if os.path.isfile(self.gamelogFileZipped): return
            url = 'http://retrosheet.org/gamelogs/' + 'gl' + self.season + ".zip"
            urllib.urlretrieve(url, filename=self.gamelogFileZipped)

    def unzip(self, type='event'):
        """
        unzips retrosheet event files for self.season of type type

        type: String | Indicates which type of event file to unzip
            (gamelog, event, etc)
        """
        if type == 'event':
            if not os.path.isfile(self.eventFileZipped):
                self.download(type='event')
            zf = zipfile.ZipFile(self.eventFileZipped)
            zf.extractall(path=self.eventFileUnzipped)
        if type == 'gamelog':
            if not os.path.isfile(self.gamelogFileZipped):
                self.download(type='gamelog')
            zf = zipfile.ZipFile(self.gamelogFileZipped)
            zf.extractall(path=self.gamelogFileUnzipped)

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

    def get_gamelog_file_zipped(self):
        return self.gamelogFileZipped

    def get_gamelog_file_unzipped(self):
        return self.gamelogFileUnzipped

