'''
Main file for the Minesweeper game
Handles game initialization, main loop, and state transitions
'''

import pygame
import sys
from gamestate_manager import GameStateManager
from main_menu import MainMenu
from Minesweeper import MineSweeper
WIDTH, HEIGHT = 400, 300

# Start point of the game
class Game:
    def __init__(self):
        pygame.init()

        # Set screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        # Initialize gamestate manager to start at main_menu
        self.gameStateManager = GameStateManager("main_menu")

        # Initialize main menu
        self.mainMenu = MainMenu(self.gameStateManager)

        # Store all possible states
        self.states = {"main_menu": self.mainMenu}

        # Start with menu’s dimensions
        self.screen = pygame.display.set_mode(
            (self.mainMenu.WIDTH, self.mainMenu.HEIGHT)
        )


    # Main game loop
    def run(self):
        while True:

            # If the user quits
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Run the current state
            state = self.gameStateManager.getState()

            # Resize window if needed
            if state == "main_menu":
                current = self.states["main_menu"]
                if self.screen.get_size() != (current.WIDTH, current.HEIGHT):
                    self.screen = pygame.display.set_mode(
                        (current.WIDTH, current.HEIGHT)
                    )
                current.run()

            # Transition to Minesweeper state
            elif state == "mine_sweeper":
                MineSweeper(self.gameStateManager).run()  # Create new instance each time
            else:
                self.states[self.gameStateManager.getState()].run()

            # Update display and tick clock
            pygame.display.update()
            self.clock.tick(30) 

if __name__ == "__main__":
    game = Game()
    game.run()
