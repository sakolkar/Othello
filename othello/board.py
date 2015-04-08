import tiles, pygame, math
from tiles import TileColor
from pygame.sprite import Sprite

UP      = (0, 1)
UP_LEFT = (-1, 1)
LEFT    = (-1, 0)
DO_LEFT = (-1, -1)
DOWN    = (0, -1)
DO_RIGHT= (1, -1)
RIGHT   = (1, 0)
UP_RIGHT= (1, 1)

class Direction():
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
    
    References:
    
    for incrementing letters in python by an index this reference was used:
    http://stackoverflow.com/questions/2156892/python-how-can-i-increment-a-char
    """
    
    # initalization
    def __init__(self,sprite_img, tile_width, tile_height, num_rows, num_cols):
        """
        """
        self._sprite = pygame.image.load(sprite_img)
        self._tile_width = tile_width
        self._tile_height = tile_height
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._board_width = self._tile_width * self._num_cols
        self._board_height = self._tile_height * self._num_rows
        
        # dictionary of 64 tiles
        self._tiles = {}
        self._highlights = {}
        
        Sprite.__init__(self)
        
        self.image = None
        self._base_image = None
        self.rect = pygame.Rect(0, 0, self._board_width, self._board_height)
                
        self._render_base_board()
        
        # count of black pieces
        self._blk_tiles = set()
        
        # count of white pieces
        self._wht_tiles = set()
        
        # list of playable tiles for black
        self._blk_playable = set()
        
        # list of playable tiles for white
        self._wht_playable = set()
    
    def _tile_count(self):
        return self._board_width * self._board_height
        
    def _tile_position(self, index):
        return (index % self._board_width, index // self._board_height)
    
    def _render_base_board(self):
        """
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
    
    def board_setup(self):
        """
        """
        # tiles (3,3) and (4,4) are white
        # tiles (4,3) and (3,4) are black
        self.set_tile(3, 3, TileColor.White)
        self.set_tile(4, 4, TileColor.White)
        self.set_tile(3, 4, TileColor.Black)
        self.set_tile(4, 3, TileColor.Black)
        
        self._blk_playable.add(self.get_tile(3,2))
        self._blk_playable.add(self.get_tile(2,3))
        self._blk_playable.add(self.get_tile(5,4))
        self._blk_playable.add(self.get_tile(4,5))
        
        self._wht_playable.add(self.get_tile(4,2))
        self._wht_playable.add(self.get_tile(5,3))
        self._wht_playable.add(self.get_tile(2,4))
        self._wht_playable.add(self.get_tile(3,5))
        
    def check_move_valid(self, tile, color):
        """
        """
        if color == TileColor.Black and tile in self._blk_playable:
            return True
        if color == TileColor.White and tile in self._wht_playable:
            return True
            
        return False
        
    def move(self, tile, color):
        """
        """
        tile_col, tile_row = tile.get_coords()
        self.set_tile(tile_row, tile_col, color)
        self.flip_tiles(tile, color)
        self.update_playable()
        
    def update_playable(self):
        """
        
        """
        
        # iterate through black tiles
        self._blk_playable = set()
        for tile in self._blk_tiles:
            for d in range(Direction.num_directions):
                i_tile = self.find_tile_in_direction(tile,
                                                     TileColor.Empty,
                                                     TileColor.White,
                                                     Direction.directions[d])
                
                if i_tile != None:
                    self._blk_playable.add(i_tile)        
        
        # iterate through white tiles
        self._wht_playable = set()
        for tile in self._wht_tiles:
            for d in range(Direction.num_directions):
                i_tile = self.find_tile_in_direction(tile,
                                                     TileColor.Empty,
                                                     TileColor.Black,
                                                     Direction.directions[d])
                
                if i_tile is not None:
                    self._wht_playable.add(i_tile)        
        
    def flip_tiles(self, tile, color):
        """
        """
        flip_color = None
        if color == TileColor.Black:
            flip_color = TileColor.White
        elif color == TileColor.White:
            flip_color = TileColor.Black
        
        for d in range(Direction.num_directions):
            i_tile = self.find_tile_in_direction(tile, 
                                                 color, 
                                                 flip_color, 
                                                 Direction.directions[d])
            
            if i_tile is not None:
                self.flip_tiles_in_direction(tile, 
                                             i_tile, 
                                             Direction.directions[d], 
                                             color)
        
    def find_tile_in_direction(self, start_tile, color, ign_color,direction):
        """
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
                    return i_tile
                else:
                    break
            elif i_tile.get_color != ign_color:
                break
            
        return None
        
    def flip_tiles_in_direction(self, start_tile, end_tile, direction, color):
        """
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
              
    # access the information of a tile
    def get_tile(self, row, col):
        """
        Find a tile on the board based on its row and column.
        
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
        
    
    # set the color of a tile
    def set_tile(self, row, col, color):
        """
        Sets a specified tile by row and column to the
        specified color. If the tile does not exist but is
        in range, the tile is created.
        
        If the tile exists then the color of the tile is
        changed to the one specified and the tile is moved
        to the corresponding set of black/white tiles.
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
        
    #def screen_coords(self, tile_coords):
    #    """
    #    Calculates the screen coordinates based on a given tile.
    #    """
    #    
    #    x, y, = tile_coords
    #    return (
    #        x * self._tile_width + self.rect.x,
    #        y * self._tile_height + self.rect.y
    #    )
        
    def update(self):
        """
        makes the board sprite to be a fresh copy of the
        _base_image. This is an empty board. The appropriate
        tiles should be drawn over this board since the
        board can change drastically from turn to turn.
        """
        self.image = self._base_image.copy()
        
        
