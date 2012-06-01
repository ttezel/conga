##`Conga`

#An AI that plays Conga
 
The game of Conga was developed by Matin Franke, and published by “Das Spiel 
Hamburg” in 1998. It is a two-player game played on a square 4X4 board, as shown below:

                     _______________________________
                    |       |       |       |       |
                    | (1,4) | (2,4) | (3,4) | (4,4) |
                    |_______|_______|______ |_______|
                    |       |       |       |       |
                    | (1,3) | (2,4) | (3,3) | (4,3) |
                    |_______|_______|_______|_______|
                    |       |       |       |       |
                    | (1,2) | (2,4) | (3,2) | (4,2) |
                    |_______|_______|_______|_______|
                    |       |       |       |       |
                    | (1,1) | (2,1) | (3,1) | (4,1) |
                    |_______|_______|_______|_______|


Initially, Player 1 has ten black stones in (1,4) and Player 2 has ten white stones in (4,1). 
The players alternate turns. On each turn, a player chooses a square with some of his 
stones in it, and picks a direction to move them, either horizontally, vertically or 
diagonally. The move is done by removing the stones from the square and placing one 
stone in the following square, two in the next one, and the others into the last one. The 
stones can only be moved in consecutive squares that are not occupied by the opponent; 
if a direction has less than three squares not occupied by the opponent in a row, then all 
remaining stones are placed in the last empty square. If a square has no neighbouring 
squares that are not occupied by the opponent, then the stones in that square cannot be 
moved. 
You can move stones from a square to a (series of) neighbouring square(s), provided the 
squares you are moving to are not occupied by the opponent. It makes no difference if the 
squares are free or occupied by yourself. You do not need any of the squares you are 
moving to be free; they could all already be occupied by your other stones. The only 
distinction is between squares that are occupied by the opponent (which block you) and squares that are not occupied by the opponent (which you can move to). 

The goal of the game is to block the opponent, so that they have no legal moves. In other 
words, all of the opponents’ stones must be trapped in squares that are all surrounded by 
the player’s stones.

Here's a screenshot of two `Agent`s playing Conga. Player 0 is playing competitively, and Player 1 is playing random moves.


![board](http://dl.dropbox.com/u/32773572/conga-bottom0.png)

----------

#`Agent`

class representing an Artifically Intelligent agent that plays Conga.

##`Agent` API

###Agent(`player`, `hfunc`, `maxDepth`)

Create an instance of `Agent`.

```python
  agent = Agent(0, 0, 3)
```

params:

####`player`
`0` for Player 1 or `1` for Player 2

####`hfunc`

Supported `hfunc` values are:

* `0`: makes move that minimizes number of moves opponent will be able to make
* `1`: makes move that maximizes the number of moves `Agent` will be able to make over opponent

This decides the score that is assigned to each board state, which decides the moves that the `Agent` makes.

####`maxDepth`

the maximum depth in the game tree that the `Agent` should explore and evaluate the score of.
I have found that a `maxDepth` of `3` provides the best performance and wins against the opponent in few moves.

###`.buildTree()`

builds the game tree for the `Agent`, scoring each node according to the heuristic function as it explores the children states of the game.
Call this function before making a move.

###`.getBestMove(state)`

given a game state, gets the next best state for the `Agent`, based on its game tree.

###`.getRandomMove(player, board)`

returns a random move for `player` to make on `board`.

params:

* `player`: `0` for Player 1 of `1` for Player 2
* `board`: **CongaBoard** instance

The output looks like this:
```python
  randMove = agent.getRandomMove(opponent.player, board)
  #{'to': [4, 2], 'from': [4, 1]}
```

###`.makeMove(fromTile, toTile, player, board)`

returns the new board state after the move is made.

params:

* `fromTile`: [x,y] of tile
* `toTile`: [x,y] of first tile in direction of move
* `player`: `0` or `1`
* `board`: **CongaBoard** instance

usage:
```python
  board = agent.makeMove([1,4], [4,1], 0, board)
```

-------

#`CongaBoard`

class representing a Conga game board.

##`CongaBoard` API
  
  creating a new game board (initialized at default state):

  ```python
    board = CongaBoard()
  ```

###`.territory`

Dict used for [ row, column ] lookups on the occupant of a tile on the board.

```python
  print 'territories:', board.territory

  print 'occupant of [4,1]', board.territory[4][1]
```

###`.amount`

Dict used for [ row, column ] lookups on the amount of pieces on a tile on the board.

```python
print 'amounts:', board.amount

print 'amount in [1,4]:', board.amount[1][4]
```

###`.draw()`

draws the Conga Board in the terminal. Each tile is colored as such: `blue` for Player 1, `red` for Player 2, and `yellow` for unnocupied tiles.

Each tile is marked with the # of pieces on that tile.

## License 

(The MIT License)

Copyright (c) 2011 Tolga Tezel &lt;tolgatezel11@gmail.com&gt;

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.