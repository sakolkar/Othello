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
        # count of white pieces
        # list of playable tiles for black
        # list of playable tiles for white
    
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
        
        if (col, row) not in self._tiles:
            self._tiles[(col, row)] = tiles.Tile(color) 
        else:
            self._tiles[(col, row)].change_color(color)
    
    
    # get the count of black/white pieces
    
    # set the count of black/white pieces (indicate privacy)
    
    # get list of playable tiles for black/white
    
    # update list of playable tiles for black/white
    
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
        
        
