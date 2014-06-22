from distutils.core import setup, Extension

CResearcher = Extension('cresearcher', 
                         include_dirs = ['uthash-master/src'],
                         sources=['cresearcher.c', 
                                  'crhelper.c', 
                                  'boxscorebuffer.c'])

setup(name='CResearcher', version='1.1', 
      description='Fully Functional finish_did_get_hit to speedup simulations.' + \
          " Now includes a hashTable data structure to speed things up even" + \
          " more.", 
      ext_modules = [CResearcher])