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
bonus for playing in the corner.

The GUI
-------

It shows you the game, and tells you who won at the end.

Credits
-------

credit to the gui file from assignment two for helping us to create our own gui.
http://stackoverflow.com/questions/510348/how-can-i-make-a-time-delay-in-python for the delay in the program
