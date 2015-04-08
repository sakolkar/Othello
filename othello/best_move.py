import board, tiles
from tiles import TileColor
from board import Direction

CORNER_COORDS = {(0,0), (0,7), (7,0), (7,0)}

def find_best_move(board, color, difficulty = 0, score = 0):
    tile = None
    cont = True
    score = 0
    high_score = 0    
    
    if color == TileColor.Black:
        playable_set = board._blk_playable
        flip_color = TileColor.White
    elif color == TileColor.White:
        playable_set = board._wht_playable
        flip_color = TileColor.Black
    else:
        raise Exception("Unspecified Team. Cannot compute best move.")
        
    for i_tile in playable_set:
        if i_tile.get_coords() in CORNER_COORDS:
            score += 10
            
        for d in range(Direction.num_directions):
            t_tile, t_score = board.find_tile_in_direction(i_tile,
                                         color,
                                         flip_color,
                                         Direction.directions[d]
                                         )
            if t_tile != None:
                score += t_score
                
        if score > high_score:
            high_score = score
            tile = i_tile
                
    if high_score > 0:
        return tile
    else:
        return None
