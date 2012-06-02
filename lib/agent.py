import copy
import random

#own modules
import congaboard
#import node

from node import Node

      
#
#   Agent class - build game tree and make moves to win
#
class Agent ():
  def __init__ (self, player, hfunc, maxDepth):
    if (player != 0 and player != 1):
      raise Exception('player must be 0 or 1')

    self.player = player
    self.opponent = 1 if player == 0 else 0
    self.hfunc = hfunc
    self.maxDepth = maxDepth

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
    num = 0
    own = self.getTiles(player, board)

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

  def updateBoard (self, board):
    self.board = board

  #get child Node of @parent with lowest heuristic value
  def getBestMove (self):
    best = float('inf')
    bestChild = None

    #update state - it is assumed to be the Agent's turn
    self.state = Node(self.player, self.board, None)

    #build game tree

    #kick off recursion with depth initialized as 0
    self.buildTree(0, self.state)

    #choose best move from game tree

    player = self.player

    print 'player', player, 'is using best move'
    choices = []
    state = self.state
    for child in state.children:
      if child.heuristicVal == best:
        choices.append(child)
      elif child.heuristicVal < best:
        choices = [ child ]
        best = child.heuristicVal

    if 0 == len(choices):
      print 'AI has no valid moves to make'
      return {}

    node = choices[int(len(choices)*random.random())]

    print 'chose',node.heuristicVal,'from',[ c.heuristicVal for c in choices ]
    return choices[int(len(choices)*random.random())]

  #
  #get heurstic value of @state for player
  #heuristic functions are defined such that their value is to be minimized
  #
  def getHeuristicValue (self, hfunc, player, opponent, state):
    if hfunc == 0:
      #number of moves opponent can make
      return self.getNumberOfMoves(opponent, state)
    elif hfunc == 1:
      #sum(# of moves opponent can make) - sum(# of moves player can make)
      return (self.getNumberOfMoves(opponent, state) - self.getNumberOfMoves(player, state))
    else:
      raise Exception('hfunc value '+hfunc+' not supported.')

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

    #get first move from first tile
    for tile in ownTiles:
      moves = self.getMovesFromTile(tile, player, state)

      #check if we are at a leaf node
      if len(moves) == 0 or self.maxDepth == depth:
        #calculate heuristic of this node
        #heuristic is # of moves your opponent can make
        heuristicVal = self.getHeuristicValue(self.hfunc, self.player, self.opponent, state)
        parent.heuristicVal = heuristicVal

        #if number of moves opponent can make is less here, then
        #propagate this up to parent all the way until it is less than a node
        if parent.parent and heuristicVal < parent.parent.heuristicVal:
          parent.parent.heuristicVal = heuristicVal

          #update parents
          self.updateHeuristics(parent.parent)
        continue

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

        self.numExplored += 1
        #recurse using the new state
        self.buildTree(depth+1, child)