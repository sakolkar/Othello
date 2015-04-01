class TileColor:
    Empty, Black, White = range(0,3)

class Tile(pygame.sprite.Sprite):
    """
    
    """
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('green_tile.png', -1)
        
    def update(self):
        pass
    
    
    
        
        
