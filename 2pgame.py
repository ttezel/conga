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


player1 = agent.Agent(0, 0, 0)

player2 = agent.Agent(1, 0, 0)

#setup new Conga board
board = congaboard.CongaBoard()

MoveCount = [ 0, 0 ]

#
# Continuously make moves until 
# one of the players can't move
#
while (True):

  def promptMove (agent, board):
    #get move from stdin
    while True:
      print '\nPlayer', agent.player, ' turn:\n'
      #prompt user
      a = raw_input('\nMove from where?\n')
      b = raw_input('\nTo where?\n')

      fromTile = [ int(num) for num in a.split(',') ]
      toTile = [ int(num) for num in b.split(',') ]

      try:
        board = agent.makeMove(fromTile, toTile, agent.player, board)
        #@player is still in the game
        MoveCount[agent.player] += 1
        break
      except:
        print 'NOT A VALID MOVE. Please try again with a valid move.'

    print '<< player', agent.player, '>> has moved:'
    board.draw()


  board.draw()
  player1.updateBoard(board)
  promptMove(player1, board)

  player2.updateBoard(board)
  promptMove(player2, board)
