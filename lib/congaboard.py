import copy
import sys

#
#   CongaBoard class - keeps state of board
#
class CongaBoard ():
  def __init__ (self):
    self.territory = {}
    self.amount = {}

    self.gameOver = False

    #initialize empty board
    for row in range (1,5):
      self.territory[row] = {}
      self.amount[row] = {}
      for col in range (1,5):
        self.territory[row][col] = -1
        self.amount[row][col] = 0

    #starting state

    #player 1 occupies 1,4 with 10 pieces
    self.territory[1][4] = 0
    self.amount[1][4] = 10

    #player 2 occupies 4,1 with 10 pieces
    self.territory[4][1] = 1
    self.amount[4][1] = 10

  def draw (self):
    keys = self.amount.keys()

    reversed = copy.deepcopy(keys)
    reversed.reverse()

    for x in keys:
      sys.stdout.write('\n')
      for y in reversed:
        #determine color to print with
        occupant = self.territory[x][y]

        if occupant == 0:
          color = '\033[94m'  #blue
        elif occupant == 1:   
          color = '\033[91m'  #red
        else:
          color = '\033[93m'  #yellow (unoccupied)

        amt = str(self.amount[x][y])

        if len(amt) == 1:
          amt = ' ' + amt

        sys.stdout.write('|' + color + amt + '\033[0m' + '|')


    sys.stdout.write('\n\n')