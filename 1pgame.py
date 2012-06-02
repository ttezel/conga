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

  #get move from stdin
  while True:

    #prompt user
    a = raw_input('\nMove from where?\n')
    b = raw_input('\nTo where?\n')

    fromTile = [ int(num) for num in a.split(',') ]
    toTile = [ int(num) for num in b.split(',') ]

    try:
      board = player.makeMove(fromTile, toTile, player.player, board)
      break
    except:
      print 'NOT A VALID MOVE. Please try again with a valid move.'

  print '<< player', player.player, '>> has moved:'
  board.draw()

  #make a new game state Node for AI to build its tree
  state = node.Node(opponent.player, board, None)


  #kick off recursion with depth initialized as 0
  opponent.buildTree(0, state)

  move = opponent.getBestMove(state)

  #end game if player cannot move
  if not move:
    #GAME OVER
    board.gameOver = True
    log(opponent.player)
    break

  #@opponent is still in the game
  MoveCount[opponent.player] += 1

  #apply the move - update @board
  board = move.board

  print '<< player ', opponent.player, '>> has moved:'