import pygame
import sys
from gamestate_manager import GameStateManager
from main_menu import MainMenu
from Minesweeper import MineSweeper

WIDTH, HEIGHT = 400, 300

#this will be the start point of the game
class Game:
    def __init__(self):
        pygame.init()

        #set screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        #initialize gamestate manager to start at main_menu
        self.gameStateManager = GameStateManager("main_menu")

        #initialize main menu
        self.mainMenu = MainMenu(self.gameStateManager)

        #store all possible states
        self.states = {"main_menu": self.mainMenu}

    def run(self):
        while True:
            # if users quits 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            #run the current state
            state = self.gameStateManager.getState()

            if state == "mine_sweeper":
                MineSweeper(self.gameStateManager).run()  # new instance each time
            else:
                self.states[self.gameStateManager.getState()].run()

            pygame.display.update()
            self.clock.tick(30) 

if __name__ == "__main__":
    game = Game()
    game.run()