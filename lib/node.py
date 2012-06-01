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
    #default value of node is Infinity
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