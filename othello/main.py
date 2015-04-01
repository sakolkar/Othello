import os, sys, pygame
from gui import GUI

if not pygame.font: print("Warning, fonts disabled")
if not pygame.mixer: print("Warning, sound disabled")

class OthelloMain:
    """
    The Main Othello Class
    """
    
    def __init__(self):
        """
        Initalize the game window
        """
        
        # initialize pygame
        pygame.init()
        pygame.display.set_caption("Othello")
        clock = pygame.time.Clock()
        main_gui = GUI()
        #pygame.mouse.set_visible(0)
        main_gui.load_board()
        
    def MainLoop(self):
        """
        Main loop of the game
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                    
                elif event.type == pygame.MOUSEBUTTONUP:
                    main_gui.on_click(event)
                
                main_gui.update()
                main_gui.draw()
                clock.tick(30) # cap at 30 fps

if __name__ == "main":
    MainWindow = OthelloMain()
    MainWindow.MainLoop()
