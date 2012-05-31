import random
import sys
import copy


iter = 0

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

        sys.stdout.write('|' + color + str(self.amount[x][y]) + '\033[0m' + '|')
    sys.stdout.write('\n\n')
      
#
#   Node class - for nodes in the game tree
#
class Node ():
  def __init__ (self, player, board, parent):
    if not isinstance(parent, Node) and not None == parent:
      raise Exception('parent must be a Node instance or `None`')

    self.player = player
    self.board = board
    self.parent = parent
    self.children = []
    #default value of node is infinity since we want to minimize the
    #heuristic value
    self.heuristicVal = float('inf')

  #children can be a Node instance or a list of them
  def addChildren (self, children):
    if isinstance(children, list):
      for child in children:
        self.addChildren(child)
      return self
    if not isinstance(children, Node):
      raise Exception('argument must be a Node instance or a list of them')
    self.children.append(children)
    return self

#
#   Agent class - build game tree and make moves to win
#
class Agent ():
  def __init__ (self, player):
    if (player != 0 and player != 1):
      raise Exception('player must be 0 or 1')

    self.player = player
    self.opponent = 1 if player == 0 else 0
    self.maxDepth = 4

    self.numExplored = 0

    print 'playing as player:', player

  #get all possible moves from a point @start
  #a move is represented as the first tile in the direction of the move
  def getMovesFromTile (self, tile, player, board):
    x = tile[0]
    y = tile[1]

    #up, up-right, right, down-right, down, down-left, left, up-left
    possible = [[x,y+1],[x+1,y+1],[x+1,y],[x+1,y-1],[x,y-1],[x-1,y-1],[x-1,y],[x-1,y+1]]

    #get allowed moves from @possible
    allowed = [ tile for tile in possible if self.isTileAllowed(tile, player, board) ]

    return allowed

  #is @tile allowed to be moved to for @player
  def isTileAllowed (self, tile, player, board):
    x = tile[0]
    y = tile[1]

    #not allowed if outside @board
    if 1 > x or 1 > y or 4 < x or 4 < y: 
      return False 

    territory = board.territory[x][y]

    if territory == -1 or territory == player:
      return True
    return False

  def getTiles (self, player, board):
    territory = board.territory
    owned = []

    for x in territory:
      for y in territory[x]:
        if territory[x][y] == player:
          owned.append([x,y])
    return owned

  #get # of moves @player can make on @board
  def getNumberOfMoves (self, player, board):
    #testing
    if 1 != player:
      raise Exception('agent should be checking player 1 not '+str(player))

    num = 0
    own = self.getTiles(player, board)

    #print 'getting number of moves player', player, 'can play'

    #increment num for each move
    for tile in own:
      num += len(self.getMovesFromTile(tile, player, board))

    return num

  def getRandomMove (self, player, board):
    print 'player', player, 'is using random move'
    pool = []
    ownTiles = self.getTiles(player, board)

    for owntile in ownTiles:
      moves = self.getMovesFromTile(owntile, player, board)
      for move in moves:
        pool.append({ 'from': owntile, 'to': move })

    poolSize = len(pool)
    
    if 0 == poolSize:
      return {}

    i = int(poolSize*random.random())
    return pool[i]

  #@board - CongoBoard instance
  #@tile - [x,y] to move from
  #@move - [x,y] first tile in direction of move
  #
  #return @result (new CongaBoard instance with move applied to it)
  def makeMove (self, tile, move, player, board):
    if not self.isTileAllowed(tile, player, board):
      raise Exception('starting tile '+str(tile)+' is not allowed for player')
    if not self.isTileAllowed(move, player, board):
      raise Exception('player cannot move to tile '+str(move))

    #print 'player', player, 'making move from', tile, 'to', move

    #we can make the move

    x0 = tile[0]
    y0 = tile[1]

    x1 = move[0]
    y1 = move[1]

    dx = x1 - x0
    dy = y1 - y0

    amount = board.amount[x0][y0]

    if amount < 1:
      raise Exception('cannot make move. No tiles at '+str(tile)+' for player '+str(player))

    #2nd tile over in direction of @move
    move2 = [x1+dx, y1+dy]

    #check if we can't move to the 2nd tile
    if not self.isTileAllowed(move2, player, board):
      #move all pieces from @tile to @move

      #update amounts
      board.amount[x0][y0] = 0
      board.amount[x1][y1] += amount

      #update territories
      board.territory[x0][y0] = -1
      board.territory[x1][y1] = player

      return board

    #we can move to 2nd tile, so let's check the 3rd one

    x2 = move2[0]
    y2 = move2[1]

    #3rd tile over in direction of @move
    move3 = [x2+dx, y2+dy]

    #check if we can't move to the 3rd tile
    if not self.isTileAllowed(move3, player, board):
      #move 1 piece to @move and all the other pieces to @move2
      
      #update amounts
      board.amount[x0][y0] = 0
      #1 piece to @move
      board.amount[x1][y1] += 1
      amount = amount - 1

      if amount < 0:
        raise Exception('should not occur')

      #the rest to @move2
      board.amount[x2][y2] += amount

      #update territories
      board.territory[x0][y0] = -1
      board.territory[x1][y1] = player
      #only update territory of 2nd tile if we actually moved piece(s) there
      if (amount > 0):
        board.territory[x2][y2] = player

      return board

    #we can move to the 3rd tile

    x3 = move3[0]
    y3 = move3[1]

    #move 1 piece to @move, 2 pieces to @move2, and the rest to @move3

    #un-occupy @tile
    board.amount[x0][y0] = 0
    board.territory[x0][y0] = -1
    
    #1 piece to @move
    board.amount[x1][y1] += 1
    board.territory[x1][y1] = player
    amount = amount - 1
    
    if (amount == 0):
      return board
    elif (1 == amount or 2 == amount):
      #put whatever @amount we have left in @move2
      board.amount[x2][y2] += amount
      board.territory[x2][y2] = player
    else:
      #put 2 in @move2
      board.amount[x2][y2] += 2
      board.territory[x2][y2] = player
      amount = amount - 2
      #put the rest in @move3
      if amount > 0:
        board.amount[x3][y3] += amount
        board.territory[x3][y3] = player

    return board

  def updateHeuristics (self, node):
    parentNode = node.parent
    val = node.heuristicVal

    while (None is not parentNode and val < parentNode.heuristicVal):
      parentNode.heuristicVal = val
      parentNode = parentNode.parent

  #get child Node of @parent with lowest heuristic value
  def getBestMove (self, node):
    best = float('inf')
    bestChild = None

    #only evaluate levels of the game tree that
    #represent the moves @player can make
    player = node.player

    print 'player', player, 'is using best move'
    choices = []
    for child in node.children:
      choices.append(child.heuristicVal)
      if child.heuristicVal < best:
        best = child.heuristicVal
        bestChild = child
    print 'chose', best, 'from', choices
    return bestChild

  #build depth-first game tree
  #
  # this game tree is a strategic one for your Agent, scoring each node
  # with the value that it represents to your Agent
  #
  #@depth - counter to keep track of recursion
  #@parent - root Node of subtree
  def buildTree (self, depth, parent):
    #get tiles occupied by me
    player = parent.player
    state = parent.board
    ownTiles = self.getTiles(player, state)
    moves = []

    global iter
    
    # iter+=1
    # if iter == 2:
    #   raise Exception('skeet')

    #get first move from first tile
    for tile in ownTiles:
      moves = self.getMovesFromTile(tile, player, state)

      #check if we are at a leaf node
      if len(moves) == 0 or self.maxDepth == depth:
        #calculate heuristic of this node
        #heuristic is # of moves your opponent can make
        opponent = 1 if 0 == parent.player else 0

        #print 'getting number of moves of opponent', opponent 

        heuristicVal = self.getNumberOfMoves(self.opponent, state)
        parent.heuristicVal = heuristicVal

        #if number of moves opponent can make is less here, then
        #propagate this up to parent all the way until it is less than a node
        if parent.parent and heuristicVal < parent.parent.heuristicVal:
          parent.parent.heuristicVal = heuristicVal

          #update parents
          self.updateHeuristics(parent.parent)
        return

      #explore child nodes since we aren't at a leaf node

      for move in moves:
        board = copy.deepcopy(state)

        #get next state of board after move
        nextState = self.makeMove(tile, move, player, board)

        #switch turn to opponent
        opponent = 1 if 0 == player else 0

        #generate the child Node state
        child = Node(opponent, nextState, parent)

        parent.addChildren(child)

        #state.draw()
        self.numExplored += 1
        #recurse using the new state
        self.buildTree(depth+1, child)

numNodes = 0
      
#
#tests
#

def log (loser):
  winner = 1 if 0 == loser else 0
  print 'GAME OVER. PLAYER ', winner, 'WINS.' 

#start as player 1
player = Agent(0)
#opponent will play random moves as player 2
opponent = Agent(1)
#setup new Conga board
board = CongaBoard()
#root state Node
state = Node(0, board, None)



#
# Continuously make moves until 
# one of the Agents can't move
#
while (True):

  #kick off recursion with depth initialized as 0
  player.buildTree(0, state)

  move = player.getBestMove(state)

  if not move:
    #GAME OVER
    board.gameOver = True
    log(player.player)
    break

  #player is still in the game
  #apply the move
  board = move.board

  print '<< player ', player.player, '>> has moved:', board.draw()

  randMove = opponent.getRandomMove(opponent.player, board)

  if not randMove:
    #GAME OVER
    board.gameOver = True
    log(opponent.player)
    break

  #opponent is still in the game
  #apply the move
  board = opponent.makeMove(randMove['from'], randMove['to'], opponent.player, board)
  #make a new Node for player to build its tree
  state = Node(player.player, board, None)

  print '<< player', opponent.player, '>> has moved:', board.draw()

  # iter+=1
  # if iter == 2:
  #   break








