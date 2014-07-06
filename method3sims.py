## Simulate round 1 method 3 simulations

from beatthestreak.npsimulation import NPSimulation as NPS

## Bogus numbers used in initialization.
sim = NPS(2010, 2009, 20, 20) # bogus numbers, just to initalize

sim.mass_simulate(
    (2010, 2010), (1, 1), (1, 300), (1, 50), (100, 600), 
    minERARAnge=(2.0, 4.0), method=3)
sim.mass_simulate(
    (2010, 2010), (1, 1), (1, 300), (51, 100), (100, 600), 
    minERARAnge=(2.0, 4.0), method=3)

## Left to do: P(101-300)