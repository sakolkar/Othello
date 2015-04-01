import os, sys, pygame, board
from pygame.sprite import LayeredUpdates
from tiles import BASE_TILE, BLK_PIECE, WHT_PIECE

#
#
#


# initalize the font
pygame.font.init()
FONT_SIZE = 16
FONT = pygame.font.SysFont("Arial", FONT_SIZE)
FONT_COLOR = (0, 0, 0)

LEFT_CLICK = 1
RIGHT_CLICK = 0

BOARD_WIDTH = 640
BOARD_HEIGHT = 640

WHITE_RGB = (255, 255, 255)

class GUI(LayeredUpdates):
    """
    
    """
    
    num_instances = 0
    
    def __init__(self, bg_color = WHITE_RGB):
        """
        
        """
        
        LayeredUpdates.__init__(self)
        
        if GUI.num_instances != 0:
            raise Exception("GUI: Another instance is already running.")
        GUI.num_instances = 1
        
        self.bg_color = bg_color
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
        self.screen_rect = pygame.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT)
        
        # set up team info. there are 2 sides black and white.
        # black always goes first
        self.num_teams = 2
        self.current_turn = 0
        self.win_team = None
        self.board = None
        
        # the tiles on the board that can be played at
        self._playable_tiles = set()
        
    @property
    def cur_team(self):
        """ 
        Gets the current team.
        Returns: 1 - team black
                 2 - team white
        """
        return ((self.current_turn) % self.num_teams) + 1
        
    def load_board(self, tile_w = 64, tile_h = 64):
        """
        Loads the game board
        """
        self.remove(self.board)
        self.board = board.Board(BASE_TILE, tile_w, tile_h)
        self.add(self.board)
        
        self.board.rect.center = self.screen_rect.center
        
        # create the inital board setup
        
    def on_click(self, event):
        """
        """
        
        # window has focus and button press was left click
        if (    event.type == pygame.MOUSEBUTTONUP
            and event.button == LEFT_CLICK
            and pygame.mouse.get_focused()):
            
            print(event.pos)
            print(self.board.tile_coords(event.pos))
            
            pass
        
    def update(self):
        """
        """
        LayeredUpdates.update(self)
        
        # update the board
        
    def draw(self):
        """
        """
        self.screen.fill(self.bg_color)
        LayeredUpdates.draw(self, self.screen)
        
        pygame.display.flip()
        
        
