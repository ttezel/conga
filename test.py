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

  player.updateBoard(board)
  bestMove = player.getBestMove()

  #end game if player cannot move
  if not bestMove:
    #GAME OVER
    board.gameOver = True
    log(player.player)
    break

  #@player is still in the game
  MoveCount[player.player] += 1

  #apply the move - update @board
  board = player.makeMove(bestMove['from'], bestMove['to'], player.player, board)

  print '<< player ', player.player, '>> has moved:', board.lastMoveMade
  board.draw()

  #opponent's turn

  opponent.updateBoard(board)

  randMove = opponent.getRandomMove()

  #end game if opponent cannot move
  if not randMove:
    #GAME OVER
    board.gameOver = True
    log(opponent.player, MoveCount)
    break

  #@opponent is still in the game
  MoveCount[opponent.player] += 1

  #apply the move
  board = opponent.makeMove(randMove['from'], randMove['to'], opponent.player, board)

  print '<< player', opponent.player, '>> has moved:', board.lastMoveMade
  board.draw()