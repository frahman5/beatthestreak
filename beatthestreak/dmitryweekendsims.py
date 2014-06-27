from npsimulation import NPSimulation as NPS

## Simulate 30-40% of the method2 simulations over the hiking trip
sim = NPS(2010, 2009, 20, 20) # bogus numbers, just to initalize
sim.mass_simulate((2010, 2010), (1,1), (1, 300), (101, 300), 
                  (100, 600), method=2)