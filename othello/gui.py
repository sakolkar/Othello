import pygame, board, best_move, time
from pygame.sprite import LayeredUpdates
from tiles import BASE_TILE, BLK_PIECE, WHT_PIECE, TileColor, TILE_W, TILE_H

# Initialize the font
pygame.font.init()
FONT_SIZE = 40
FONT = pygame.font.SysFont("Arial", FONT_SIZE, bold=True)
FONT_COLOR = (0, 0, 0)

# define gui constants
LEFT_CLICK = 1
RIGHT_CLICK = 0
BOARD_WIDTH = 512
BOARD_HEIGHT = 512
NUM_ROWS = 8
NUM_COLS = 8
NUM_TEAMS = 2
START_TURN = 0
BOARD_TOP_PAD = int((BOARD_HEIGHT - (TILE_H * NUM_ROWS))/2)
BOARD_LEFT_PAD = int((BOARD_WIDTH - (TILE_W * NUM_COLS))/2)
WHITE_RGB = (255, 255, 255)
BLACK_RGB = (0, 0, 0)
SEMI_TRANSPARENT = 128

CPU_COLOR = TileColor.White

class GUI(LayeredUpdates):
    """
    GUI class handles all the user input and game handling.
    Initialization of GUI creates a pygame game window.
    """
    
    num_instances = 0
    
    def __init__(self, bg_color = WHITE_RGB):
        """
        Creates a game window with the specified GUI 
        constants.Ensures that only one instance of the GUI
        is running.
        """
        
        LayeredUpdates.__init__(self)
        
        if GUI.num_instances != 0:
            raise Exception("GUI: Another instance is already running.")
        GUI.num_instances += 1
        
        self.bg_color = bg_color
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
        self.screen_rect = pygame.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT)
        
        # set up team info. there are 2 sides black and white.
        # black always goes first
        self.num_teams = NUM_TEAMS
        self.current_turn = START_TURN
        self.win_team = None
        self.board = None
        
    @property
    def cur_team(self):
        """ 
        Gets the current team.
        Returns: 1 - team black
                 2 - team white
        """
        return int(((self.current_turn) % self.num_teams) + 1)
        
    def load_board(self, tile_w = TILE_W, tile_h = TILE_H):
        """
        Loads the game board's default configuration:
        Two black tiles and two white tiles in cross pattern
        at the centre of the board
        """
        
        self.remove(self.board)
        self.board = board.Board(BASE_TILE, tile_w, tile_h, NUM_ROWS, NUM_COLS)
        self.add(self.board)
        
        # position the board image in the center of the
        # game window. This is necessary as the game window
        # may have a larger resolution than the game board
        self.board.rect.center = self.screen_rect.center
        
        # create the inital board setup
        self.board.board_setup()
        
    def on_click(self, event):
        """
        Handle left click mouse events in the game window.
        Determines if the mouse click was a valid tile for
        the current team and registers the click as a move
        for the current team.
        """
        
        # check if window has focus and button press was
        # left click
        if (event.type == pygame.MOUSEBUTTONUP
            and event.button == LEFT_CLICK
            and pygame.mouse.get_focused()):
            
            col, row = self.board.tile_coords(event.pos)
            
            tile_clicked = self.board.get_tile(row, col)
            
            # only register clicks on the board
            if row not in range(NUM_ROWS) or col not in range(NUM_COLS):
                return
                
            # discard clicks on already used tiles
            if tile_clicked.get_color != TileColor.Empty:
                return
                
            # discard clicks on invalid tile locations
            if not self.board.check_move_valid(tile_clicked, self.cur_team):
                return
            
            self.board.move(tile_clicked, self.cur_team)
            self.update()
            self.draw()
            
            self.next_turn()
            
            # play the computer's turn
            if self.cur_team == CPU_COLOR:
                #time.sleep(1)
                c_move, n_flip = best_move.find_best_move(self.board, 
                                                          self.cur_team)
                if c_move != None:
                    self.board.move(c_move, self.cur_team)
                self.next_turn()
                
        
    def update(self):
        """
        handles updating the sprites to be displayed
        in the game window
        """
        LayeredUpdates.update(self)
        
    def draw(self):
        """
        handles drawing the sprites onto the game window
        """        
        self.screen.fill(self.bg_color)
        LayeredUpdates.draw(self, self.screen)
        
        # draw the tiles onto the board sprite
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                area = pygame.Rect(0, 0, TILE_W, TILE_H)
                
                self.screen.blit(self.board.get_tile(i,j)._sprite, 
                                 (j*TILE_W + BOARD_LEFT_PAD, 
                                 i*TILE_H + BOARD_TOP_PAD),
                                 area)
            
        if self.win_team == None:
            # update the full contents of the screen
            pygame.display.flip()
        
    def next_turn(self):
        """
        moves the game onto the next player.
        Note: next_turn() should be called even if there
              are no valid moves for the player. Such a
              turn is a "pass" but a turn nonetheless.
        """       
        self.current_turn += 1
        # see if the new team has valid moves        
        self.check_valid_moves_exist()
        
        
    def check_valid_moves_exist(self):
        """
        determines if the current team has any valid moves.
        if there are no valid moves, it will check if the
        opposing team has valid moves. If the opposing team
        does have valid moves it registers a "pass" for the
        current team. Otherwise it will register an endgame
        by setting a winning team.
        """
        if self.cur_team == TileColor.Black and \
            self.board.num_playable_blk_tiles == 0:
                
            if self.board.num_playable_wht_tiles == 0:
                self.calculate_winning_team()
            else:
                self.current_turn += 1
            
        if self.cur_team == TileColor.White and \
            self.board.num_playable_wht_tiles == 0:     
                
            if self.board.num_playable_blk_tiles == 0:
                self.calculate_winning_team()
            else:
                self.current_turn += 1
                
    def calculate_winning_team(self):
        """
        sets the winning team by setting the teams color in
        self.win_team.
        If the game is tied then the "empty" color will be
        set in win_team.
        """
        if self.board.num_black > self.board.num_white:
            self.win_team = TileColor.Black
        elif self.board.num_white > self.board.num_black:
            self.win_team = TileColor.White
        else:
            self.win_team = TileColor.Empty
            
    def draw_endgame(self):
        """
        draws the endgame screen. displays the team that
        won.
        """
        endgame_rect = self.screen_rect
        width = self.screen.get_width()
        height = self.screen.get_height()
        endgame_overlay = pygame.Surface((width, height))
        endgame_overlay.fill(BLACK_RGB)
        endgame_overlay.set_alpha(SEMI_TRANSPARENT)
        self.screen.blit(endgame_overlay, (0,0))
        
        gameover_text_surf = FONT.render("Game Over!", 1, WHITE_RGB)
        gover_w = gameover_text_surf.get_width()
        text_h = 0
        self.screen.blit(gameover_text_surf, ((width/2 - gover_w/2), text_h))
        text_h += gameover_text_surf.get_height()
        
        if self.win_team == TileColor.Empty:
            endgame_string = "TIED!"
        elif self.win_team == TileColor.Black:
            endgame_string = "BLACK WINS!"
        elif self.win_team == TileColor.White:
            endgame_string = "WHITE WINS!"
        winteam_text_surf = FONT.render(endgame_string, 1, WHITE_RGB)
        wteam_w = winteam_text_surf.get_width()
        self.screen.blit(winteam_text_surf, ((width/2 - wteam_w/2),text_h))
        
        pygame.display.flip()
