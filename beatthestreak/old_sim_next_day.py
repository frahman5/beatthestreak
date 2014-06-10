 today = self.get_date()

        # check if today featured a suspended game
        suspGameToday = False
        if today in self.susGamesDict.keys():
            suspGameToday = True

        # progress indicator
        if self.get_date().day % 10 == 0: 
            print "Simming day: {0}".format(today) 

        # Retrieve list of players playing today
        activePlayers = [player for player in self.players if \
             Researcher.did_start(today, player)]

        # assign players to bots and update histories
        mod_factor = len(activePlayers)
        if mod_factor == 0: # no activePlayers today
            self.incr_date()
            return 
        for i, bot in enumerate(self.bots):
            player = activePlayers[i % mod_factor]

            # Case 1: Unsuspended game (99.9% of games)
            hitVal = Researcher.did_get_hit(today, player)
            other = None

            if suspGameToday: # Case 2: Suspended games, may need to ovveride
                pRID = player.get_retrosheet_id()
                susGameParticipants = self.susGamesDict[today][1]
                if pRID in susGameParticipants:
                    if self.susGamesDict[today][0]: # Case 2.1: Valid, Suspended
                        # hitVal stays the same, other gets overriden
                        other = specialCasesD['S']['V']
                    elif not self.susGamesDict[today][0]: # Case 2.2: Invalid, Suspended
                        # override both hitVal and other
                        hitVal = 'pass'
                        other = specialCasesD['S']['I']

            bot.update_history(player, hitVal, today, other=other)

        # update the date
        self.incr_date()