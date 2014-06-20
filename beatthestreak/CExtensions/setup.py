from distutils.core import setup, Extension

expModule = Extension('experiment', sources=['experiment.c'])

setup(name='Experiment', version='0.1', 
      description='This is an experiment package', 
      ext_modules = [expModule])