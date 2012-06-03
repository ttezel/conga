from lib import agent
from lib import congaboard
from lib import node

#
# end-of-game logging
#

def log (loser, movecount):
  winner = 1 if 0 == loser else 0
  print 'GAME OVER. PLAYER ', winner, 'WINS.'

  for p in range(0,2):
    print 'player', p, ':  moved', movecount[p], 'times'



#human will play as player 1
player = agent.Agent(0, 0, 0)

#AI plays as player 2 with maxDepth 3
opponent = agent.Agent(1, 0, 3)

#setup new Conga board
board = congaboard.CongaBoard()

MoveCount = [ 0, 0 ]

#
# Continuously make moves until 
# one of the Agents can't move
#
while (True):
  board.draw()
  player.updateBoard(board)

  #get move from stdin
  while True:

    #prompt user
    a = raw_input('\nMove from where?\n')
    b = raw_input('\nTo where?\n')

    fromTile = [ int(num) for num in a.split(',') ]
    toTile = [ int(num) for num in b.split(',') ]

    try:
      board = player.makeMove(fromTile, toTile, player.player, board)
      #@player is still in the game
      MoveCount[player.player] += 1
      break
    except:
      print 'NOT A VALID MOVE. Please try again with a valid move.'

  print '<< player', player.player, '>> has moved:'
  board.draw()

  opponent.updateBoard(board)

  bestMove = opponent.getBestMove()

  #end game if player cannot move
  if not bestMove:
    #GAME OVER
    board.gameOver = True
    log(opponent.player)
    break

  #@opponent is still in the game
  MoveCount[opponent.player] += 1

  #apply the move - update @board
  board = opponent.makeMove(bestMove['from'], bestMove['to'], opponent.player, board)

  print '<< player ', opponent.player, '>> has moved:'