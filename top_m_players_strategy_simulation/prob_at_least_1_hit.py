## Calculate the probability that given m players with batting averages
## greater than or equal to .300, at least one player gets a hit on a given
## day.

from operator import mul
from fractions import Fraction

def nCk(n,k):
    return int(reduce(mul, (Fraction(n-i, i+1) for i in range(k)), 1))

def calc_probability(m, min_batting_average=.300):
    sum = 0
    for num_players in range(1,m):
        comb = nCk(m, num_players)
        successes = min_batting_average**num_players
        failures = (1-min_batting_average)**(m-num_players)
        sum += comb * successes * failures
    return sum
        
               
        
