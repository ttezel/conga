##`Conga`

#An AI that plays Conga

Here's a screenshot as it plays against an Agent that makes random moves:

* Player 0 is Agent
* Player 1 is Agent that plays random moves

![board](http://dl.dropbox.com/u/32773572/conga-bottom0.png)

The AI is created with the following keys:
  * `player`
  * `hfunc`
  * `maxDepth`

`player`

* `0` for Player 1
* `1` for Player 2

##`Agent` API

Creating an instance of `Agent`:

```python
  #instance playing as Player 1, using heuristic function 0 and maxDepth of 3
  agent = Agent(0, 0, 3)
```

`hfunc`

Supported `hfunc` values are:

* `0`: makes move that minimizes number of moves opponent will be able to make
* `1`: makes move that maximizes the number of moves player will be able to make over opponent

This decides the score that is assigned to each board state, which decides the moves that the Agent makes.

`maxDepth`

the maximum depth in the game tree that the Agent should explore and evaluate the score of.
I have found that a `maxDepth` of `3` provides the best performance and wins against the opponent in few moves.

-------

#`CongaBoard`

class representing a Conga game board.

##`Conga` API
  
  creating a new game board (initialized at default state):

  ```python
    board = CongaBoard()
  ```

###`.draw()`

draws the Conga Board in the terminal.

* `blue` for Player 1
* `red` for Player 2
* `yellow` for unnocupied tiles

Each tile is marked with the # of pieces the player has on that tile

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