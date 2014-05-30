import os
import shutil

from data import Data

def setup():
	# Clean out zipped file folder of everything
    zippedFileFolder = Data.rootDir + Data.defaultDestZippedSuffix
    os.chdir(zippedFileFolder)
    for file in os.listdir(os.getcwd()): os.remove(file)

    # Clean out unzipped file folder as well
    unzippedFileFolder = Data.rootDir + Data.defaultDestUnzippedSuffix
    os.chdir(unzippedFileFolder)
    for file in os.listdir(os.getcwd()): 
      if os.path.isdir(file): 
        shutil.rmtree(file)
      else: 
        os.remove(file) 

def teardown():
    # Clean out zipped file folder afterwards
    zippedFileFolder = Data.rootDir + Data.defaultDestZippedSuffix
    os.chdir(zippedFileFolder)
    for file in os.listdir(os.getcwd()): 
      if os.path.isdir(file): 
        shutil.rmtree(file)
      else: 
        os.remove(file) 

    # Clean out unzipped file folder as well
    unzippedFileFolder = Data.rootDir + Data.defaultDestUnzippedSuffix
    os.chdir(unzippedFileFolder)
    for file in os.listdir(os.getcwd()): 
      if os.path.isdir(file): 
        shutil.rmtree(file)
      else: 
        os.remove(file) 
