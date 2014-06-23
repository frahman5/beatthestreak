test: crhelper.c testcresearcher.c boxscorebuffer.c
	gcc crhelper.c testcresearcher.c boxscorebuffer.c -I /Users/faiyamrahman/\
	programming/Python/beatthestreak/beatthestreak/CExtensions/CResearcher/uthash-master/src -o test
python:
	python setup.py build -g
	python setup.py install
testgdb: crhelper.c testcresearcher.c boxscorebuffer.c
	sudo ulimit -c unlimited	
	gcc -g crhelper.c testcresearcher.c boxscorebuffer.c -I /Users/faiyamrahman/\
	programming/Python/beatthestreak/beatthestreak/CExtensions/CResearcher/uthash-master/src -o test
