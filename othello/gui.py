import sys, pygame
from pygame.sprite import LayeredUpdates
#
#
#


# initalize the font
pygame.font.init()
FONT_SIZE = 16
FONT = pygame.font.SysFont("Arial", FONT_SIZE)
FONT_COLOR = (0, 0, 0)

BASE_TILE = "/assets/green_tile.png"
BLK_PEICE = "/assets/black_peice.png"
WHT_PEICE = "/assets/white_peice.png"

LEFT_CLICK = 1
RIGHT_CLICK = 0

BOARD_WIDTH = 640
BOARD_HEIGHT = 640

class GUI(LayeredUpdates):
    """
    
    """
    
    num_instances = 0
    
    def __init__(self):
        """
        
        """
        
        LayeredUpdates.__init__(self)
        
        if GUI.num_instances != 0:
            raise Exception("GUI: Another instance is already running.")
        GUI.num_instances = 1
        
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
        self.screen_rect = pygame.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT)
        
        # set up team info. there are 2 sides black and white.
        # black always goes first
        self.num_teams = 2
        self.current_turn = 0
        self.win_team = None
        self.map = None
        
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
        
    def load_board(self, tile_w = 80, tile_h = 80):
        """
        Loads the game board
        """
        self.remove(self.map)
        self.map = board.Board(BASE_TILE, tile_w, tile_h)
        self.add(self.map)
        
        self.map.rect.center = self.screen_rect.center
        
        # create the inital board setup
        
    def on_click(self, event):
        """
        """
        
        # window has focus and button press was left click
        if (    event.type == pygame.MOUSEBUTTONUP
            and event.button == LEFT_CLICK
            and pygame.mouse.get_focused()):
            
            
            pass
        
        
        
        
