import tiles, pygame, math
from tiles import TileColor
from pygame.sprite import Sprite

# define direction constants
# (col_dir, row_dir)
UP      = (0, 1)
UP_LEFT = (-1, 1)
LEFT    = (-1, 0)
DO_LEFT = (-1, -1)
DOWN    = (0, -1)
DO_RIGHT= (1, -1)
RIGHT   = (1, 0)
UP_RIGHT= (1, 1)

# enumerate direction constants
class Direction():
    """
    holds the information for the directions that ar can be
    legally travelled along on the othello board from any
    tile. the direction is specified by (col_dir, row_dir)
    
    Direction.num_direction gives the total number of
        directions.
        
    Direction.direction[i] gives the corresponding 
        (col_dir,row_dir) for the direction i
    """
    num_directions = 8
    directions = {0:UP, 
                  1:UP_LEFT, 
                  2:LEFT, 
                  3:DO_LEFT,
                  4:DOWN, 
                  5:DO_RIGHT, 
                  6:RIGHT, 
                  7:UP_RIGHT}

# board datastructure that holds all the tiles
class Board(Sprite):
    """  
    A Board Class that handles setting tiles on the board
    and making various moves. Handles flipping the tiles
    when valid moves are made and determines if tiles can
    be played at by either team.
    """
    def __init__(self,sprite_img, tile_width, tile_height, num_rows, num_cols):
        """
        initializes a standard empty board and creates the 
        necessary sprite information for drawing the board.
        """
        self._sprite = pygame.image.load(sprite_img)
        self._tile_width = tile_width
        self._tile_height = tile_height
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._board_width = self._tile_width * self._num_cols
        self._board_height = self._tile_height * self._num_rows
        
        Sprite.__init__(self)
        
        self.image = None
        self._base_image = None
        self.rect = pygame.Rect(0, 0, self._board_width, self._board_height)
        
        # dictionary of 64 tiles
        self._tiles = {}
        self._highlights = {}
        
        # count of black pieces
        self._blk_tiles = set()
        
        # count of white pieces
        self._wht_tiles = set()
        
        # list of playable tiles for black
        self._blk_playable = set()
        
        # list of playable tiles for white
        self._wht_playable = set()
        
        self._render_base_board()
    
    def _render_base_board(self):
        """
        Creates a sprite surface of the empty board.
        """
        # create the empty surface
        self._base_image= pygame.Surface((self._board_width,self._board_height))
        
        # draw in each tile
        for i in range(self._num_rows):
            for j in range(self._num_cols):
                self.set_tile(i, j, TileColor.Empty)
                area = pygame.Rect(0, 0, self._tile_width, self._tile_height)
                self._base_image.blit(self._sprite, 
                                      (j*self._tile_width, 
                                      i*self._tile_height),
                                      area)    
    
    @property
    def num_playable_blk_tiles(self):
        """
        the number of tiles black can play at in the next turn
        """
        return len(self._blk_playable)
        
    @property
    def num_playable_wht_tiles(self):
        """
        the number of tiles white can play at in the next turn
        """
        return len(self._wht_playable)
        
    @property
    def num_black(self):
        """
        the number of black tiles currently on the board
        """
        return len(self._blk_tiles)
        
    @property
    def num_white(self):
        """
        the number of white tiles currently on the board
        """
        return len(self._wht_tiles)
    
    def board_setup(self):
        """
        sets up the standard layout of the board. Two white
        pieces and two black pieces at the center of the
        board crossed from each other.
        """
        # tiles (3,3) and (4,4) are white
        # tiles (4,3) and (3,4) are black
        self.set_tile(3, 3, TileColor.White)
        self.set_tile(4, 4, TileColor.White)
        self.set_tile(3, 4, TileColor.Black)
        self.set_tile(4, 3, TileColor.Black)
        
        self.update_playable()
        
    def check_move_valid(self, tile, color):
        """
        Checks if a tile can be played at by the team of
        the specified color.
        
        Inputs:
            tile - desired tile to be played at
            color- color of the team wanting to play
            
        Returns:
            True - if the tile can be played at by the team
            False- if the tile cannot be played at.
        """
        if color == TileColor.Black and tile in self._blk_playable:
            return True
        if color == TileColor.White and tile in self._wht_playable:
            return True
            
        return False
        
    def move(self, tile, color):
        """
        handles a move made by them team with the specified
        color at the given tile.
        
        Inputs:
            tile - the tile played at by the team
            color- the team's color
        """
        tile_col, tile_row = tile.get_coords()
        self.set_tile(tile_row, tile_col, color)
        self.flip_tiles(tile, color)
        self.update_playable()
        
    def update_playable(self):
        """
        updates the sets:
            _blk_playable
            _wht_playable
        by iterating through each tile and finding valid
        tiles where each team can play at in the next turn.
        """
        # iterate through black tiles
        self._blk_playable = set()
        for tile in self._blk_tiles:
            for d in range(Direction.num_directions):
                i_tile, num_ign_tiles = self.find_tile_in_direction(tile,
                                                     TileColor.Empty,
                                                     TileColor.White,
                                                     Direction.directions[d])
                
                if i_tile != None:
                    self._blk_playable.add(i_tile)        
        
        # iterate through white tiles
        self._wht_playable = set()
        for tile in self._wht_tiles:
            for d in range(Direction.num_directions):
                i_tile, num_ign_tiles = self.find_tile_in_direction(tile,
                                                     TileColor.Empty,
                                                     TileColor.Black,
                                                     Direction.directions[d])
                
                if i_tile is not None:
                    self._wht_playable.add(i_tile)        
        
    def flip_tiles(self, tile, color):
        """
        Flips all the tiles that should be flipped from a
        move at the specified tile by the team with the
        specified color.
        
        Inputs:
            tile - the tile that was just played at
            color- the color of the tile that was just
                   played.
        """
        flip_color = None
        if color == TileColor.Black:
            flip_color = TileColor.White
        elif color == TileColor.White:
            flip_color = TileColor.Black
        
        for d in range(Direction.num_directions):
            # find the tile in a directoin with the same color
            i_tile, n_flip = self.find_tile_in_direction(tile, 
                                                        color, 
                                                        flip_color, 
                                                        Direction.directions[d])
            
            if i_tile is not None:
                # flip tiles until the tile of the same color
                self.flip_tiles_in_direction(tile, 
                                             i_tile, 
                                             Direction.directions[d], 
                                             color)
        
    def find_tile_in_direction(self, start_tile, color, ign_color, direction):
        """
        Find the tile of a desired color in a specified
        direction skipping over tiles that have the color
        of ign_color.
        
        Inputs:
            start_tile - the tile to begin the search from
            color      - the color of the tile being
                         searched for.
            ign_color  - an ignore color. tiles of this
                         color are skipped over
            direction  - the direction in which to look for
                         the tile. from Direction.direction
                         
        Returns:
            (Tile, ign_tiles_passed)
            Tile - the tile that was being searched for and
                   has the desired color.
            ign_tiles_passed - the number of tiles with the
                               ign_color.
                               
        Example:
        If there are two white tiles the second tile left of
        the first with 5 black tiles in between, calling:
        
            self.find_tile_in_direction(start_tile = white_tile_1,
                                        color = TileColor.White,
                                        ign_color = TileCOlor.Black,
                                        Direction.direction[2])
                                        
        will return:
            (white_tile_2, 5) 
        since 5 black tiles were ignored when going in the
        left direction when looking for the second white tile.
        """
        tile_col, tile_row = start_tile.get_coords()
        tile_not_found = True
        i_tile = start_tile
        ign_tiles_passed = 0
        
        while tile_not_found:
            tile_col += direction[0]
            tile_row += direction[1]
            
            # make sure new row and col are in range
            if tile_row not in range(self._num_rows) or \
               tile_col not in range(self._num_cols):
                break
            
            i_tile = self.get_tile(tile_row, tile_col)
            if i_tile.get_color == ign_color:
                ign_tiles_passed += 1
            elif i_tile.get_color == color:
                tile_not_found = False
                if ign_tiles_passed > 0:
                    return i_tile, ign_tiles_passed
                else:
                    break
            elif i_tile.get_color != ign_color:
                break
            
        return None, ign_tiles_passed
        
    def flip_tiles_in_direction(self, start_tile, end_tile, direction, color):
        """
        Flip the tiles to the specified color between the
        specified start tile and the specified end tile.
        
        Inputs:
            start_tile - the tile from which to start flipping
                         the tiles' colors
            end_tile   - the tile at which to stop flipping
                         the tiles
            direction  - the direction in which to flip tiles
                         to get to end_tile from start_tile
                         from Direction.direction
            color      - the desired color after the tiles
                         is flipped.
        """
        if start_tile == end_tile:
            return
        
        i_col, i_row = start_tile.get_coords()
        e_col, e_row = end_tile.get_coords()
        
        all_tiles_not_flipped = True
        
        while all_tiles_not_flipped:
            i_col += direction[0]
            i_row += direction[1]
            
            i_tile = self.get_tile(i_col, i_row)
            
            if i_col == e_col and i_row == e_row:
                all_tiles_not_flipped = False
                
            self.set_tile(i_row, i_col, color)
              
    def get_tile(self, row, col):
        """
        Find a tile on the board based on its row and column.
        
        Inputs:
            row - the row of the desired tile
            col - the column of the desired tile
        
        Return: Tile()
        """
        if row not in range(self._num_rows) or \
           col not in range(self._num_cols):
            raise Exception("Attempted to access invalid tile ({},{})".format(
                            col, row))
        
        if (col, row) not in self._tiles:
            raise Exception("Tile ({},{}) not defined.".format(col, row))
        else:
            return self._tiles[(col, row)]
        
    def set_tile(self, row, col, color):
        """
        Sets a specified tile by row and column to the
        specified color. If the tile does not exist but is
        in range, the tile is created.
        
        If the tile exists then the color of the tile is
        changed to the one specified and the tile is moved
        to the corresponding set of black/white tiles.
        
        Inputs:
            row - the desired tile's row
            col - the desired tile's column
            color - the desired color for the tile
        """
        if row not in range(self._num_rows) or \
           col not in range(self._num_cols):
            raise Exception("Attempted to access invalid tile ({},{})".format(
                            col, row))
            
        tile = None
        
        if (col, row) not in self._tiles:
            self._tiles[(col, row)] = tiles.Tile(color, col = col, row = row) 
        else:
            tile = self.get_tile(row, col)
            if tile.get_color == TileColor.Black:
                self._blk_tiles.remove(tile)
            if tile.get_color == TileColor.White:
                self._wht_tiles.remove(tile)
            tile.change_color(color)
        
        # add the tile to the set of current black/white tiles
        if color == TileColor.Black:
            self._blk_tiles.add(tile)  
        if color == TileColor.White:
            self._wht_tiles.add(tile)
    
    def tile_coords(self, screen_coords):
        """
        Finds the column, row for a specified screen pos.
        
        return: (col, row)
        """
        x, y, = screen_coords
        return (
            math.floor((x - self.rect.left) / self._tile_width),
            math.floor((y - self.rect.top) / self._tile_height)
        )
        
    def update(self):
        """
        makes the board sprite to be a fresh copy of the
        _base_image. This is an empty board. The appropriate
        tiles should be drawn over this board since the
        board can change drastically from turn to turn.
        """
        self.image = self._base_image.copy()
