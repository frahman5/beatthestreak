## Simulate round 1 method 3 simulations

from beatthestreak.npsimulation import NPSimulation as NPS

## Bogus numbers used in initialization.
sim = NPS(2010, 2009, 20, 20) # bogus numbers, just to initalize

#sim.mass_simulate(
 #   (2010, 2010), (1, 1), (1, 300), (201, 250), (100, 600), 
  #  minERARange=(2.0, 4.0), method=3)
sim.mass_simulate(
    (2010, 2010), (1, 1), (1, 300), (251, 300), (100, 600), 
    minERARange=(2.0, 4.0), method=3)
