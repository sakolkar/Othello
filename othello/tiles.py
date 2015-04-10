import os, pygame

PRG_DIR_PATH = os.path.abspath(os.path.dirname(os.path.dirname("tiles.py")))
AST_DIR_PATH = os.path.join(PRG_DIR_PATH, "assets")

# find the path for the tile images
BASE_TILE = os.path.join(AST_DIR_PATH, "green_tile.png")
BLK_PIECE = os.path.join(AST_DIR_PATH, "black_piece.png")
WHT_PIECE = os.path.join(AST_DIR_PATH, "white_piece.png")

# tile image constants
TILE_W = 64
TILE_H = 64

# enumerate the tile colors
class TileColor:
    Empty, Black, White = range(0,3)

class Tile(pygame.sprite.Sprite):
    """
    A Tile class that can hold information about a tile's
    color location and sprite image.
    """
    def __init__(self, color, row = None, col = None):
        """
        Initialize the tile and give it a base sprite image
        of an empty tile.
        """
        pygame.sprite.Sprite.__init__(self)
        self._color = TileColor.Empty
        self._sprite = pygame.image.load(BASE_TILE)
        self._base_image = self._sprite
        self._row = row
        self._col = col
        
    def change_color(self, color):
        """
        Changes the color of the tile to the specified color.
        
        Inputs:
            color - the color to change the tile to
        """
        tile_rect = pygame.Rect(0,0,TILE_W, TILE_H)
        
        if color == TileColor.Black:
            self._color = TileColor.Black
            self._base_image.blit(pygame.image.load(BLK_PIECE), tile_rect)
            
        elif color == TileColor.White:
            self._color = TileColor.White
            self._base_image.blit(pygame.image.load(WHT_PIECE), tile_rect)
            
    @property
    def get_color(self):
        """
        Get the current color of the tile
        
        Return: color - from TileColor()
        """
        return self._color
    
    def get_coords(self):
        """
        Get the location of the tile on a board.
        
        Return: (column, row)
        """
        return self._col, self._row
        
    def update(self):
        """
        Updates the sprite image of the tile.
        """
        self.image = self._base_image.copy()
