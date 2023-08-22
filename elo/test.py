
from elo import Elo

eloLeague = Elo(k = 20, homefield=0)
eloLeague.addPlayer("Daniel", rating = 1600)
eloLeague.addPlayer("Harry", rating = 1600)
eloLeague.expectResult(eloLeague.ratingDict['Daniel'],eloLeague.ratingDict['Harry'])
print(eloLeague.ratingDict)
eloLeague.gameOver(winner = "Daniel", loser = "Harry", winnerHome=True)
print(eloLeague.ratingDict)
eloLeague.gameOver(winner = "Daniel", loser = "Harry", winnerHome=True)
print(eloLeague.ratingDict)
eloLeague.gameOver(winner = "Daniel", loser = "Harry", winnerHome=True)
print(eloLeague.ratingDict)
eloLeague.gameOver(winner = "Daniel", loser = "Harry", winnerHome=True)
print(eloLeague.ratingDict)