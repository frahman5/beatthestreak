# simulate 

from npsimulation import NPSimulation as NPS

## Bogus numbers used in initialization.
sim = NPS(2010, 2009, 20, 20) # bogus numbers, just to initalize
sim.mass_simulate((2010, 2010), (1,1), (1, 300), (201, 250), 
                  (100, 600), method=2)

## STILL LEFT TO DO: P:251-300