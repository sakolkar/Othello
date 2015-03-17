import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print("Warning, fonts disabled")
if not pygame.mixer: print("Warning, sound disabled")

class OthelloMain:
    """
    The Main Othello Class
    """
    
    def __init__(self, width=512, height=512):
        """
        Initalize the game window
        """
        
        # initialize pygame
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        
    def MainLoop(self):
        """
        Main loop of the game
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    
if __name__ == "__main__":
    MainWindow = OthelloMain()
    MainWindow.MainLoop()
