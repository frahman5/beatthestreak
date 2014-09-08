This project relies on data from the Lahman and Retrosheet baseball
data repositories to simulate different beat the streak strategies. 

MLB's beat the streak is a fantasy game that challenges users to 
correctly predict players who will get a hit 57 times in a row (with some
caveats). 

I built this simulation purely for personal use, and as such there may be
some bugs. 

USAGE:

./npsimulation.py [OPTIONS] simYear batAveYear N P
   
   -> runs a single simulation with given parameters and options

Options:

   -d : DoubleDown. If not provided, default is SingleDown

   -sM=[METHODNUMBER]: Indicate simulation method. METHODNUMBER is an int
                       If -sM=3 or -sM=4 is chosen, must provide -mE

   -mE=[MINERA]: Indicate minimum era to be used if sM=3 or sM=4. Must be 
                 a positive rational number.

   -mP=[minPlateAppearnces]: Indicate minimum number of plate appearances
                             that a player must have had to qualify for the sim
                             If not provided, defaults to 502
                             
   -t : indicates results should be printed to test results folder

