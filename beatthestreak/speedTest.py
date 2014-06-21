#! pyvenv/bin/python
import sys

from datetime import date

from researcher import Researcher as R
from player import Player


c_did_get_hit = R.c_did_get_hit
did_get_hit = R.did_get_hit

pL = Player('jonesch06', 2003)
MC1 = Player("Miguel", "Cabrera", 2012)
MC2 = Player("Asdrubal", "Cabrera", 2012)
dateMC = date(2012, 9, 5)
MY1 = Player("Michael", "Young", 2012)
MY2 = Player("Delmon", "Young", 2012)
dateMY = date(2012, 6, 26)
Lance = Player("Lance", "Berkman", 2008)
p1 = Player("Edwin", "Jackson", 2012)
p2 = Player("Jose", "Reyes", 2012, debut='6/10/2003')
p3 = Player("Alfonso", "Soriano", 2012)
p4 = Player("Jorge", "Posada", 2010)
p5 = Player("Manny", "Ramirez", 2008) # season he got traded 

def main(*args):
    # correct number of args
    assert len(args) == 2
    if args[1] == '-c': # c version
        get_hit_func = c_did_get_hit
    elif args[1] == '-p': # p version
        get_hit_func = did_get_hit
    else:
        raise Exception("Usage is ./speedTest.py -c OR ./speedTest.py -p")
    for i in range(0, 10):
        get_hit_func(date(2012, 5, 2), p1)
        get_hit_func(date(2012, 6, 16), p2)
        get_hit_func(date(2005, 4, 4), p2)
        get_hit_func(date(2003, 7, 12), p2)
        get_hit_func(date(2012, 6, 15), p2)
        get_hit_func(date(2008, 9, 21), p2)
        get_hit_func(date(2003, 3, 31), p3)
        get_hit_func(date(2009, 5, 12), p3)
        get_hit_func(date(2001, 9, 4), p3)
        get_hit_func(date(2007, 7, 20), p3)
        get_hit_func(date(2004, 9, 16), p3)
        get_hit_func(date(2004, 8, 17), p4)
        get_hit_func(date(2010, 7, 11), p4)
        get_hit_func(date(1997, 5, 23), p4)
        get_hit_func(date(2000, 4, 30), p4)
        get_hit_func(date(1994, 7, 26), p5)
        get_hit_func(date(2008, 5, 22), p5)
        get_hit_func(date(2008, 8, 1), p5)
        get_hit_func(date(1995, 6, 30), p5)
        get_hit_func(date(2008, 7, 29), p5)
        get_hit_func(date(2008, 8, 31), p5)
        get_hit_func(date(2003, 4, 19), pL)
        get_hit_func(date(2003, 8, 28), pL)
        get_hit_func(dateMC, MC1)
        get_hit_func(dateMC, MC2)
        get_hit_func(dateMY, MY1)
        get_hit_func(dateMY, MY2)
        get_hit_func(date(1996, 9, 25), p4)
        get_hit_func(date(2008, 9, 7), p2)
        get_hit_func(date(2007, 7, 28), p2)
        get_hit_func(date(2006, 6, 3), p2)
        get_hit_func(date(2009, 7, 9), Lance)
    return

if __name__ == '__main__':
    """
    Usage:
    1) ./speedTest.py -c
    2) ./speedTest.py -p
    """
    main(*sys.argv)