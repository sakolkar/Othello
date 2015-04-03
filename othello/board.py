import tiles, pygame, math
from tiles import TileColor
from pygame.sprite import Sprite

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
        pass
        
        
    def flip_tiles(self, tile, color):
        """
        """
        
        # check left of the tile
        i_tile = self.find_tile_in_direction(tile, color, -1, 0)
        self.flip_tiles_in_direction(tile, i_tile, -1, 0, color)
        
        # check right of the tile
        i_tile = self.find_tile_in_direction(tile, color, 1, 0)
        self.flip_tiles_in_direction(tile, i_tile, 1, 0, color)
        
        # check below the tile
        i_tile = self.find_tile_in_direction(tile, color, 0, -1)
        self.flip_tiles_in_direction(tile, i_tile, 0, -1, color)
        
        # check above the tile
        i_tile = self.find_tile_in_direction(tile, color, 0, 1)
        self.flip_tiles_in_direction(tile, i_tile, 0, 1, color)
        
        # check up-right diagonal
        i_tile = self.find_tile_in_direction(tile, color, 1, 1)
        self.flip_tiles_in_direction(tile, i_tile, 1, 1, color)
        
        # check up-left diagonal
        i_tile = self.find_tile_in_direction(tile, color, -1, 1)
        self.flip_tiles_in_direction(tile, i_tile, -1, 1, color)
        
        # check bot-right diagonal
        i_tile = self.find_tile_in_direction(tile, color, 1, -1)
        self.flip_tiles_in_direction(tile, i_tile, 1, -1, color)
        
        # check bot-left diagonal
        i_tile = self.find_tile_in_direction(tile, color, -1, -1)
        self.flip_tiles_in_direction(tile, i_tile, -1, -1, color)
        
    def find_tile_in_direction(self, tile, color, col_dir, row_dir):
        """
        """
        tile_col, tile_row = tile.get_coords()
        tile_not_found = True
        i_tile = tile
        
        while tile_not_found:
            tile_col += col_dir
            tile_row += row_dir
            
            # make sure new row and col are in range
            if tile_row not in range(self._num_rows) and \
               tile_col not in range(self._num_cols):
                break
            
            i_tile = self.get_tile(tile_row, tile_col)
            
            if i_tile.get_color() == TileColor.Empty:
                break
            elif i_tile.get_color() == color:
                tile_not_found = False
                return i_tile
            
        return tile
        
    def flip_tiles_in_direction(self, start_tile, end_tile, col_dir, row_dir, color):
        """
        """
        
        if start_tile == end_tile:
            return
        
        i_col, i_row = start_tile.get_coords()
        e_col, e_row = end_tile.get_coords()
        
        all_tiles_not_flipped = True
        
        while all_tiles_not_flipped:
            i_col += col_dir
            i_row += row_dir
            
            i_tile = self.get_tile(i_col, i_row)
            
            if i_col == e_col and i_row == e_row:
                all_tiles_not_flipped = False
                
            self.set_tile(i_row, i_col, color)
              
    # access the information of a tile
    def get_tile(self, row, col):
        """
        """
        
        if row not in range(self._num_rows) and \
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
        
        columns are lettered in the gui
        rows are numbered in the gui
        
        """
        if row not in range(self._num_rows) and \
           col not in range(self._num_cols):
            #col = chr(ord('A') + col)
            raise Exception("Attempted to access invalid tile ({},{})".format(
                            col, row))
            
        tile = None
        
        if (col, row) not in self._tiles:
            self._tiles[(col, row)] = tiles.Tile(color, col = col, row = row) 
        else:
            tile = self.get_tile(row, col)
            if tile.get_color() == TileColor.Black:
                self._blk_tiles.remove(tile)
            if tile.get_color() == TileColor.White:
                self._wht_tiles.remove(tile)
            tile.change_color(color)
            
        if color == TileColor.Black:
            self._blk_tiles.add(tile)
            
        if color == TileColor.White:
            self._wht_tiles.add(tile)
    
    
    # get the count of black/white pieces
    
    # get list of playable tiles for black/white
    
    # get the tile at coordinates
    def tile_coords(self, screen_coords):
        """
        """
        x, y, = screen_coords
        return (
            math.floor((x - self.rect.left) / self._tile_width),
            math.floor((y - self.rect.top) / self._tile_height)
        )
        
    def screen_coords(self, tile_coords):
        """
        """
        
        x, y, = tile_coords
        return (
            x * self._tile_width + self.rect.x,
            y * self._tile_height + self.rect.y
        )
        
    def update(self):
        """
        
        """
        # copy over the base image
        self.image = self._base_image.copy()
        
        
