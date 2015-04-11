Othello
=======

CMPUT 275 Wednesday Friday
Final Project
Justin Aardema
Satyen Akolkar

Installing/Running
------------------

To run the game, enter the command in the Othello directory:
(the Othello directory contains /assests /othello and README.md)

    /Othello$ python3 othello difficulty
    
where difficulty is an integer. For smooth running of the
program. It is reccommended to run at a difficulty less than
or equal to 6.Here is an example of running the game at a
difficulty of 4:

    /Othello$ python3 othello 4
    
Gameplay
--------
 
The game starts in the classic Othello set up, a square in the
middle of the board, with two black pieces corner to corner, and 
two white pieces also corner to corner. The player goes first, and 
controls black.  They click in an place that turns a white piece(there
is a white piece directly between the played piece and another, already
played, black piece).  After this, the computer goes, and then control
is shifted back to the player.  The game ends when there are no more moves
for either player, usually because the board is filled.  At this point, the 
person with the most pieces is declared the winner, and they celebrate.

The A.I. plans the best move based on an algorithim that judges the best move
for how many pieces it flips, and will let it flip in the future, as well as a
bonus for playing in the corner. The runtime for this algorithm is O(64^n) where
n is the difficulty chosen. As you can see this means that the algorithm becomes
quite time intensive very quickly. The reccommended difficulty is 6 where the
game remains challenging but not too time consuming by waiting on the computer
for extremely long.

How to Play
-----------
1. You are team black and make the first move.
2. Click on an empty tile where you MUST flip at least one white tile
3. Wait for the computer to respond with its move.
4. Repeat steps 2&3 until no team has any valid moves or the board is
   filled.
5. If you cannot make any valid moves (you cannot flip at least one white
   tile) your turn will be "passed."
6. If you are playing at high difficulty (>=6) be patient with the computer
   as it will take time to think about its move, much like you would think
   about yours.
7. If you feel that the computer should've played a move but hasn't the
   most likely possibility that occured is that there were no valid moves
   for the computer, so it "passed" its turn.

The GUI
-------

It shows you the game, and tells you who won at the end.

Credits
-------

credit to the gui file from assignment two for helping us to create our own gui.
http://stackoverflow.com/questions/510348/how-can-i-make-a-time-delay-in-python for the delay in the program
