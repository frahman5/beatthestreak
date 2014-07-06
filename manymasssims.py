from beatthestreak.npsimulation import NPSimulation as NPS

## Bogus numbers used in initialization.
sim = NPS(2010, 2009, 20, 20) # bogus numbers, just to initalize

# print "EXPECT: DID_START, DETERMINISTIC"
# # Method1, doubleDown
# sim.mass_simulate((2010, 2010), (1,1), (10, 20), (20, 25), 
#                   (100, 100), method=1)

# print "EXPECT: DID_START, RANDOM"
# # Method2, singleDown
# sim.mass_simulate((2010, 2010), (1,1), (10, 20), (20, 25), 
#                   (100, 100), method=2)

# print "EXPECT: DID_START AND ERA, DETERMINISTIC"
# # Method3, singleDown
# sim.mass_simulate((2010, 2010), (1,1), (10, 20), (20, 25), 
#                   (100, 100), minERARange=(1.0, 2.5), method=3)


print "EXPECT: DID_START AND ERA, RANDOM"
# Method4, singleDown
sim.mass_simulate((2010, 2010), (1,1), (10, 20), (20, 25), 
                  (100, 100), minERARange=(1.0, 2.5), method=4)
