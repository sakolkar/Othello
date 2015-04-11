import sys, board, tiles
from tiles import TileColor
from board import Direction

# define the coordinates of the corner tiles
CORNER_COORDS = {(0,0), (0,7), (7,0), (7,0)}
BREAK_EARLY = float("inf")
NEG_INFINITY = -1*float("inf")

try:
    if sys.argv[1]:
        DIFFICULTY = int(float(sys.argv[1]))
except:
    DIFFICULTY = 6
    
if DIFFICULTY > 10:
    DIFFUICULTY = 10

def find_best_move(board, color, diff = DIFFICULTY):
    """
    Finds the best tile for a team to move at in the turn.
    Depending upon the difficulty it will recursively call
    itself increasing the score based on maximizing the 
    current team's pieces and minimizing the opposing teams
    pieces.
    
    Inputs:
        board - the board on which the teams are playing
        color - the current team's color
        diff  - difficulty an integer representing the 
                number of turns to look ahead on the board.
                
    Returns:
        tile - the tile at which the current team should
               play for the best move.
    """    
    tile = None
    cont = True
    score = 0
    high_score = NEG_INFINITY  
    difficulty = diff
    
    if diff == 0:
        BREAK_EARLY = float("inf")
    else:
        BREAK_EARLY = 100/diff
    
    if color == TileColor.Black:
        playable_set = board.get_playable_black_tiles()
        flip_color = TileColor.White
    elif color == TileColor.White:
        playable_set = board.get_playable_white_tiles()
        flip_color = TileColor.Black
    else:
        raise Exception("Unspecified Team. Cannot compute best move.")
        
    for i_tile in playable_set:
        # set bias for corner position pieces
        if i_tile.get_coords() in CORNER_COORDS:
            score += 15
            
        # increase score for each tile flipped
        for d in range(Direction.num_directions):
            t_tile, t_score = board.find_tile_in_direction(i_tile,
                                         color,
                                         flip_color,
                                         Direction.directions[d]
                                         )
            if t_tile != None:
                score += t_score
        
        # break early if the score is sufficiently high
        if score >= BREAK_EARLY:
            high_score = score
            tile = i_tile
            break
        
        # depending on difficulty "look ahead" to see the move's effect
        # on the board
        if difficulty > 0:
            opp_tile, opp_score = find_best_move(board, flip_color,difficulty-1)
            score -= opp_score
            
        if score > high_score:
            high_score = score
            tile = i_tile
    
    # return the tile and the score
    if high_score > NEG_INFINITY:
        return tile, high_score
    else:
        return None, 0
