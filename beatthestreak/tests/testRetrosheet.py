import unittest
import os
import tests

from data import Data
from tests import setup, teardown, r2013, eventfiles2013, boxscores2013, \
    teamAbbrevs2013

# @unittest.skip("Focus is not in Retrosheet right now")
class TestRetrosheet(unittest.TestCase):

    def setUp(self):
        tests.setup()
        
    def tearDown(self):
        tests.teardown()

    def test_download(self):
        # test that we can download event files
        r2013.download(type='event')
        self.assertTrue(os.path.isfile(r2013.get_event_file_zipped()))

        # test that we can download gamelog files
        r2013.download(type='gamelog')
        self.assertTrue(os.path.isfile(r2013.get_gamelog_file_zipped()))

    def test_unzip(self):
        # test that we can unzip event files
        r2013.download(type='event') # assume works
        r2013.unzip(type='event')
        self.assertTrue(os.path.isfile(r2013.get_event_file_unzipped() + \
                                           "/2013ANA.EVA"))
        self.assertTrue(os.path.isfile(r2013.get_event_file_unzipped() + \
                                           "/2013OAK.EVA"))

        # test that we can unzip gamelog files
        r2013.download(type='gamelog') # assume works
        r2013.unzip(type='gamelog')
        self.assertTrue(os.path.isfile(Data.get_unzipped_gamelog_path(2013)))

    def test_gen_team_abbrevs(self):
        r2013.download() # assume works
        r2013.unzip() # assume works
        self.assertEqual(r2013.gen_team_abbrevs(),teamAbbrevs2013)

    def test_gen_boxscores(self):
        r2013.download() # assume works
        r2013.unzip() # assume works
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