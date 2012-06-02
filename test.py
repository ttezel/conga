from lib import agent
from lib import congaboard
from lib import node

#
#tests
#

def log (loser, movecount):
  winner = 1 if 0 == loser else 0
  print 'GAME OVER. PLAYER ', winner, 'WINS.'

  for p in range(0,2):
    print 'player', p, ':  moved', movecount[p], 'times'

#start as player 1 with maxDepth of 3
player = agent.Agent(0, 0, 3)
#opponent will play random moves as player 2
opponent = agent.Agent(1, 0, 0)
#setup new Conga board
board = congaboard.CongaBoard()

MoveCount = [ 0, 0 ]





#root state Node
#state = node.Node(0, board, None)

#
# Continuously make moves until 
# one of the Agents can't move
#
while (True):

  ######
  #new API tests
  player.updateBoard(board)
  move = player.getBestMove()

  #end game if player cannot move
  if not move:
    #GAME OVER
    board.gameOver = True
    log(player.player)
    break

  #@player is still in the game
  MoveCount[player.player] += 1

  #apply the move - update @board
  board = move.board

  print '<< player ', player.player, '>> has moved:', move.board.draw()

  randMove = opponent.getRandomMove(opponent.player, board)

  if not randMove:
    #GAME OVER
    board.gameOver = True
    log(opponent.player, MoveCount)
    break

  #opponent is still in the game
  MoveCount[opponent.player] += 1

  #apply the move
  board = opponent.makeMove(randMove['from'], randMove['to'], opponent.player, board)
  #make a new Node for player to build its tree
  state = node.Node(player.player, board, None)

  print '<< player', opponent.player, '>> has moved:', board.draw()