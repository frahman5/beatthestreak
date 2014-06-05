import unittest
import os

from beatthestreak.filepath import Filepath
from beatthestreak.tests import setup, teardown, r2013, eventfiles2013, \
    boxscores2013, teamAbbrevs2013

class TestRetrosheet(unittest.TestCase):

    def setUp(self):
        setup()
        
    def tearDown(self):
        teardown()

    def test_download(self):
        # test that we can download event files
        r2013.download(typeT='event')
        self.assertTrue(os.path.isfile(r2013.get_event_file_zipped()))

        # test that we can download gamelog files
        r2013.download(typeT='gamelog')
        self.assertTrue(os.path.isfile(r2013.get_gamelog_file_zipped()))

    def test_unzip(self):
        # test that we can unzip event files
        r2013.unzip(typeT='event')
        self.assertTrue(os.path.isfile(r2013.get_event_file_unzipped() + \
                                           "/2013ANA.EVA"))
        self.assertTrue(os.path.isfile(r2013.get_event_file_unzipped() + \
                                           "/2013OAK.EVA"))

        # test that we can unzip gamelog files
        r2013.unzip(typeT='gamelog')
        self.assertTrue(os.path.isfile(Filepath.get_retrosheet_file(
            folder='unzipped', fileF='gamelog', year=2013)))

    def test_gen_team_abbrevs(self):
        self.assertEqual(r2013.gen_team_abbrevs(),teamAbbrevs2013)

    def test_gen_boxscores(self):
        r2013.gen_boxscores()
        for path in boxscores2013:
            self.assertTrue(os.path.isfile(r2013.get_dest_unzipped() + \
                              "/events2013/" + path))

    def test_clean_used_files(self):
        r2013.download() # assume works
        r2013.unzip() # assume works 

        # Are the files there before we begin?
        for path in eventfiles2013:
            self.assertTrue(os.path.isfile(r2013.get_dest_unzipped() + \
                                          "/events2013/" + path))
        # Clean 'em' out and check that theyre gone
        r2013.clean_used_files()
        for path in eventfiles2013:
            self.assertFalse(os.path.isfile(r2013.get_dest_unzipped() + \
                                            "/events2013/" + path))
