from distutils.core import setup, Extension

CResearcher = Extension('cresearcher', 
                         sources=['cresearcher.c', 'crhelper.c'])

setup(name='CResearcher', version='0.1', 
      description='This is just to get it to fail tests', 
      ext_modules = [CResearcher])