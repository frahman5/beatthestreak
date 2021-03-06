from distutils.core import setup, Extension

CResearcher = Extension('cresearcher', 
                         include_dirs = ['uthash-master/src'],
                         extra_compile_args= ['-std=c99', '-g', '-O0'],
                         sources=['cresearcher.c', 
                                  'crhelper.c', 
                                  'boxscoreBuffer.c', 
                                  'playerInfoCache.c'])

setup(name='CResearcher', version='2.0', 
      description='Now includes cget_hit_info function',
      ext_modules = [CResearcher])
