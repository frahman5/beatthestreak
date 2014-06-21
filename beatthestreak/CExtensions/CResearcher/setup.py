from distutils.core import setup, Extension

CResearcher = Extension('cresearcher', 
                         sources=['cresearcher.c', 'crhelper.c'])

setup(name='CResearcher', version='1.0', 
      description='Fully Functional finish_did_get_hit to speedup simulations', 
      ext_modules = [CResearcher])