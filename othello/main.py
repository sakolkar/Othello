import sys, pygame
from gui import GUI

if not pygame.font: print("Warning, fonts disabled")
if not pygame.mixer: print("Warning, sound disabled")

MAX_FPS = 60

class OthelloMain:
    """
    The Main Othello Class. Initalizing this class creates 
    a game window using the GUI class and loads a default
    Othello board.
    """
    
    def __init__(self):
        """
        Initalize the game window and load a default Othello
        board.
        """        
        # initialize pygame
        pygame.init()
        pygame.display.set_caption("Othello")
        self.clock = pygame.time.Clock()
        self.main_gui = GUI()
        self.main_gui.load_board()
        
    def MainLoop(self):
        """
        Main loop of the game. Monitors for events in the
        game window. If the "x" is pressed it closes the
        game. Also the mouse click events are forwarded to
        the GUI.on_click() function. The game window is also
        updated everytime an event is processed.
        """        
        while True:
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                    
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.main_gui.on_click(event)
                
            self.main_gui.update()
            self.main_gui.draw()
            
            if self.main_gui.win_team != None:
                self.main_gui.draw_endgame()
                
            self.clock.tick(MAX_FPS)

if __name__ == "main":    
    # initalize the game window
    MainWindow = OthelloMain()
    
    # start the game loop
    MainWindow.MainLoop()
