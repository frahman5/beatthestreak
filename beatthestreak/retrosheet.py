import urllib
import os
import shutil
import zipfile
import subprocess

from filepath import Filepath
from exception import NoRetrosheetTypeException

class Retrosheet(object):
    """
    A Retrosheet API to download event files and parse them
    for relevant boxscores

    Data:
        Season: String | Indicates which season's event files this
            object handles (format: yyyy)
        destZipped: String | Indicates where zipped event files go
        destUnzipped: String | Indicates where unzipped files go
        eventFileZipped: String | Path of zipped event file
        eventFolderUnzipped: String | Path of directory of unzipped event files
        gamelogFolderUnzipped: String | Path of directory of unzipped gamelog files
        gamelogFileZIpped: String | Path of zipped gamelog file
        gamelogFileUnzipped: String | Path of unzipped gamelog file
        FileTypes: TupleOfStrings | Retrosheet file types supported
    """
    def __init__(self, season):
        assert type(season) == int
        self.season = season

        self.destZipped = Filepath.get_retrosheet_folder(folder='zipped')
        self.destUnzipped = Filepath.get_retrosheet_folder(folder='unzipped')

        self.eventFileZipped = Filepath.get_retrosheet_file(folder='zipped', 
            fileF='event', year=season)
        self.eventFolderUnzipped = Filepath.get_retrosheet_folder(
            folder='unzipped', subFolder='events', year=season)

        self.gamelogFolderUnzipped = Filepath.get_retrosheet_folder(
            folder='unzipped', subFolder='gamelog', year=season)
        self.gamelogFileZipped = Filepath.get_retrosheet_file(
            folder='zipped', fileF='gamelog', year=season)
        self.gamelogFileUnzipped = Filepath.get_retrosheet_file(
            folder='unzipped', fileF='gamelog', year=season)

        self.FileTypes = ('gamelog', 'event')
    
    def download_and_unzip(self, typeT='event'): # pragma: no cover
        """
        string -> None
        type: which kind of retrosheet files to download and unzip

        Downloads and unzips retrosheet files of type type
        """
        assert type(typeT) == str
        assert typeT in self.FileTypes

        self.download(typeT=typeT)
        self.unzip(typeT=typeT)
        
    def download(self, typeT='event'):
        """
        string -> None
        typeT: string | which type of retrosheet files to download
            typeT must be in ('gamelog', 'event')

        downloads retrosheet files for self.season of type typeT
        """
        assert type(typeT) == str
        assert typeT in self.FileTypes

        if typeT == 'event':
            if os.path.isfile(self.eventFileZipped): return
            url = 'http://www.retrosheet.org/events/' + \
                str(self.get_season()) + "eve.zip"
            urllib.urlretrieve(url, filename=self.eventFileZipped)
            return 
        if typeT == 'gamelog':
            if os.path.isfile(self.gamelogFileZipped): return
            url = 'http://retrosheet.org/gamelogs/' + 'gl' + \
                str(self.get_season()) + ".zip"
            urllib.urlretrieve(url, filename=self.gamelogFileZipped)
            return
        else: # pragma: no cover
            raise NoRetrosheetTypeException("Invalid retrosheet download" + \
                " type: {0}".format(typeT))

    def unzip(self, typeT='event'):
        """
        string -> None
        typeT: String | Indicates which type of event file to unzip
            typeT must be one of ('gamelog', 'event')

        unzips retrosheet event files for self.season of type typeT
        """
        assert type(typeT) == str
        assert typeT in self.FileTypes

        if typeT == 'event':
            if not os.path.isfile(self.eventFileZipped):
                self.download(typeT='event')
            zf = zipfile.ZipFile(self.eventFileZipped)
            zf.extractall(path=self.eventFolderUnzipped)
            return
        if typeT == 'gamelog':
            if not os.path.isfile(self.gamelogFileZipped):
                self.download(typeT='gamelog')
            zf = zipfile.ZipFile(self.gamelogFileZipped)
            zf.extractall(path=self.gamelogFolderUnzipped)
            return
        else: # pragma: no cover
            raise NoRetrosheetTypeException("Invalid retrosheet unzip" + \
                " type: {0}".format(typeT))

    def gen_boxscores(self):
        """
        None -> None

        Generates boxscores for each team in season self.season.
        Requires that play-by-play event files have been unzipped to 
            self.destUnzipped
        Stores boxscores in .txt files in self.destUnzipped
        """
        # If necessary event files are not present, go get them
        if not os.path.isdir(self.eventFolderUnzipped):
            self.download_and_unzip(typeT='event')

        # get the list of team abbreviations for self.season
        teamAbbrevs = self.gen_team_abbrevs()
 
        # use cwbox command line tool to generate boxscores 
        # from event files for each team
        callPrefix = ['cwbox', '-a', '-y', str(self.get_season())]
        os.chdir(self.destUnzipped + "/events" + str(self.get_season()))
        for team in teamAbbrevs:
            call = callPrefix + [str(self.get_season()) + team[0] \
                + ".EV" + team[1]]
            with open(str(self.get_season()) + team[0] + "B" + \
                ".txt", "w+") as file:
                subprocess.call(call, stdout=file)

    def gen_team_abbrevs(self):
        """
        None -> None

        Extracts 3 letter abbreviations and league affiliation for all 
        MLB teams in season self.season from file teamyyyy 
        where yyyy = self.season
        """
        # If necessary event files are not present, go get them
        if not os.path.isdir(self.eventFolderUnzipped):
            self.download_and_unzip(typeT='event')

        # open team file and read team abbrevations from it    
        teamPath = self.eventFolderUnzipped + "/team" + str(self.get_season())
        with open(teamPath, "r") as f:
            teamAbbrevs = [(line.split(',')[0], line.split(',')[1]) for
                                line in f]
        return teamAbbrevs

    def clean_used_files(self):
        """
        Removes all zipped retrosheet files, as well as used event files

        To be used after necessary information has been extracted and parsed
        """
        # navigate to unzipped folder, then remove all ".EVA", ".EVN" files and
        # the team file
        os.chdir(Filepath.get_retrosheet_folder(folder='unzipped',
            subFolder='events', year=self.get_season()))
        [os.remove(file) for file in os.listdir(os.getcwd()) 
            if file.endswith(".EVA") or file.endswith(".EVN") or 
            file.endswith("team" + str(self.get_season()))]

        # navigate to zipped folder and remove all ".zip" files
        os.chdir(self.get_dest_zipped())
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
        return self.eventFolderUnzipped

    def get_gamelog_file_zipped(self):
        return self.gamelogFileZipped

    def get_gamelog_file_unzipped(self): # pragma: No cover
        return self.gamelogFileUnzipped

