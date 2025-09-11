# how to install pygames - https://www.geeksforgeeks.org/installation-guide/how-to-install-pygame-in-windows/
# Pygames documentation - https://www.pygame.org/docs/
#                         https://coderslegacy.com/python/python-pygame-tutorial/

import pygame           # Imports pygame library
import sys              #Imports sys library
import BoardGenerator   #Imports BoardGenerator
from grid import Grid

# ---------- RGB variables ----------
black = (0, 0, 0)          # Black color
white = (255, 255, 255)    # White color
blue = (0, 0, 255)         # Blue color

# ---------- App window ----------
grid_width = 10   # Number of grid columns (width)
grid_height = 10  # Number of grid rows (height)
grid_size = 32        # Size of each grid square in pixels
border = 16           # General border size (left, right, bottom)
top_border = 25      # Top border size for menu/spacing
app_width = grid_size * grid_width + border * 2  # App window width in pixels
app_height = grid_size * grid_height + border + top_border  # App window height in pixels

# ---------- Game loop (to be implemented) ----------
bg_color = (192, 192, 192) # Background gray color
grid_color = (128, 128, 128) # Grid line gray color

class MineSweeper:
    def __init__(self, gameStateManager):
        pygame.init()
        # Creates main pygame window
        self.gameDisplay = pygame.display.set_mode((app_width, app_height))

        self.clock = pygame.time.Clock()  # control FPS
        
        #set game state manager
        self.gameStateManager = gameStateManager
        
        pygame.display.set_caption("Minesweeper")  # Set window title to "Minesweeper"
        
        #track if grid has been generated
        self.initialized = False

    # ---------- Utility function ----------
    def drawText(self, txt, s, yOff=0):
        """
        Draws text centered on the game screen.
        txt  = text string
        s    = font size
        yOff = vertical offset for placement
        """
        screen_text = pygame.font.SysFont("Calibri", s, True).render(txt, True, blue)  # Creates a font surface Object
        rect = screen_text.get_rect()  # Get rectangle boundary of text
        # Center text in the grid area with vertical offset
        rect.center = (grid_width * grid_size / 2 + border, 
                    grid_height * grid_size / 2 + top_border + yOff)
        self.gameDisplay.blit(screen_text, rect)  # Draws text to screen
    
    def initialize_minesweeper(self):
        
        # get number of mines from state manager
        params = self.gameStateManager.getParams()
        #set to 10 if param set to num
        numMine = params.get("numMine", 10)

        # ---------- Program entry point ----------
        #print(f"gameloop start... \nNumber of Mines = {numMine}")  # Debug print to console

        # 1. Create bomb grid (10x10 with bombs randomly placed)
        raw_grid = BoardGenerator.generate_bombs(numMine)
        #2. Create numbering for adjacent mines
        raw_grid = BoardGenerator.generate_numbering(raw_grid)

        # #-> Prints raw_grid
        # print("Heres raw_grid:")
        # BoardGenerator.print_grid(raw_grid)
    
        # 2. Convert raw grid into Grid objects
        self.grid = [[Grid(x, y, "b" if raw_grid[y][x] == 'b' else int(raw_grid[y][x]), self.gameDisplay, border, top_border, grid_size) for x in range(grid_width)] for y in range(grid_height)]
        self.mines = [(x, y) for y in range(grid_height) for x in range(grid_width) if raw_grid[y][x] == 'b']

        self.game_win = False
        self.game_over = False
        
        self.initialized = True

    def run(self):
            if not self.initialized:
                self.initialize_minesweeper()

            while not self.game_over:
                #handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        for row in self.grid:
                            for cell in row:
                                if cell.rect.collidepoint(mouse_pos): #If mouse click is within cell
                                    if event.button == 1:  #Left click
                                        if not cell.flag: #Only allow cell to be revealed if not flagged
                                            cell.clicked = True #Reveal cell
                                    elif event.button == 3:  #Right click
                                        cell.toggleFlag() #Place flag

                # Draw grid
                #Create off-screen frame buffer
                frame_surface = pygame.Surface((app_width, app_height))
                frame_surface.fill((192, 192, 192))  # background
                for row in self.grid:
                    for cell in row:
                        cell.drawGrid(frame_surface)

                #Blit buffer to main display
                self.gameDisplay.blit(frame_surface, (0,0))
                pygame.display.flip()  # flip once per frame
                self.clock.tick(30)

            #logic for when game is over
            self.gameStateManager.setState("main_menu")
            self.initialized = False  # reset for next game

    def gameLoop(self, grid, mines):
       pass 
