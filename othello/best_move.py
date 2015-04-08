import board, tiles
from tiles import TileColor

def find_best_move(board, color, difficulty, score):
    tile = None
    cont = True
    score = 0
    high_score = 0
    best_tile = None
    row_check = [-1, 0, 1]
    column_check = [-1, 0, 1]
    

    if color == TileColor.Black:
        for tiles in self._blk_playable:
            if tiles.get_cords() = 0,0:
                score += 10
            if tiles.get_cords() = 7,7:
                score += 10
            if tiles.get_cords() = 0,7:
                score += 10
            if tiles.get_cords() = 7,0:
                score += 10
            for x in row_check:
                for y in column_check:
                    while cont = True:
                        if find_tile_in_direction(tiles, Black, x, y).get_color == TileColor.White:
                            temp_score += 1
                            tiles_col += x
                            tiles_row += y
                        elif find_tile_in_direction(tiles, Black, x, y).get_color == TileColor.Black:
                            cont = False
                        elif find_tile_in_direction(tiles, Black, x, y).get_color == TileColor.Out:
                            cont = False
                            #change tileset and board file to fit this!
                        elif find_tile_in_direction(tiles, Black, x, y).get_color == TileColor.Empty:
                            #change needed to board file! (the return when not in range or empty)
                            score += temp_score
                            cont = False
            if score > high_score:
                high_score = score
                tile = tiles

    elif color == TileColor.White:
        for tiles in self._wht_playable:
            if tiles.get_cords() = 0,0:
                score += 10
            if tiles.get_cords() = 7,7:
                score += 10
            if tiles.get_cords() = 0,7:
                score += 10
            if tiles.get_cords() = 7,0:
                score += 10
            for x in row_check:
                for y in column_check:
                    while cont = True:
                        if find_tile_in_direction(tiles, White, x, y).get_color == TileColor.Black:
                            temp_score += 1
                            tiles_col += x
                            tiles_row += y
                        elif find_tile_in_direction(tiles, White, x, y).get_color == TileColor.White:
                            cont = False
                        elif find_tile_in_direction(tiles, White, x, y).get_color == TileColor.Out:
                            cont = False
                            #change tileset and board file to fit this!
                        elif find_tile_in_direction(tiles, White, x, y).get_color == TileColor.Empty:
                            #change needed to board file! (the return when not in range or empty)
                            score += temp_score
                            cont = False
            if score > high_score:
                high_score = score
                best_tile = tiles

    return tile
