import os, pygame

PRG_DIR_PATH = os.path.abspath(os.path.dirname(os.path.dirname("tiles.py")))
AST_DIR_PATH = os.path.join(PRG_DIR_PATH, "assets")

BASE_TILE = os.path.join(AST_DIR_PATH, "green_tile.png")
BLK_PIECE = os.path.join(AST_DIR_PATH, "black_piece.png")
WHT_PIECE = os.path.join(AST_DIR_PATH, "white_piece.png")

TILE_W = 64
TILE_H = 64

class TileColor:
    Empty, Black, White = range(0,3)

class Tile(pygame.sprite.Sprite):
    """
    
    """
    
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self._color = TileColor.Empty
        self._sprite = pygame.image.load(BASE_TILE)
        
    def change_color(self, color):
        """
        """
        tile_rect = pygame.Rect(0,0,TILE_W, TILE_H)
        
        if color == TileColor.Black:
            self._color = TileColor.Black
            self._sprite.blit(pygame.image.load(BLK_PIECE), tile_rect)
            print("BLACK")
        elif color == TileColor.White:
            self._color = TileColor.White
            self._sprite.blit(pygame.image.load(WHT_PIECE), tile_rect)
            print("WHITE")
        
    def update(self):
        self.image = self._sprite.copy()
    
    
    
        
        
