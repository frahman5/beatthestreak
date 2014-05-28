# Load the CSV of batter stats
batter.stats <- read.csv("Batting.csv")
# Take a subset with only playerids, total hitts, total at bats, year 2012
relevant = subset(batter.stats, yearID == 2011, c("playerID", "AB", "H", "yearID"))
# Add a variable (column): season batting average
relevant$BattingAve <- with(relevant, (H / AB))
batting.aves.sans.nans = rapply(list(relevant$BattingAve), f=function(x) ifelse(is.nan(x), 0, x), how="replace")
best = max(unlist(batting.aves.sans.nans))

## To do when you get back -> qualify the batting ave with num_hits over a certain number
## Also return the player id, then get the name of that player using master.csv
## and print the name