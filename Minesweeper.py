# how to install pygames - https://www.geeksforgeeks.org/installation-guide/how-to-install-pygame-in-windows/
# Pygames documentation - https://www.pygame.org/docs/
#                         https://coderslegacy.com/python/python-pygame-tutorial/

import pygame           # Imports pygame library
import sys              #Imports sys library
import BoardGenerator   #Imports BoardGenerator
pygame.init()  # Initializes all imported pygame modules

# ---------- RGB variables ----------
black = (0, 0, 0)          # Black color
white = (255, 255, 255)    # White color
blue = (0, 0, 255)         # Blue color

# ---------- App window ----------
grid_width = 10   # Number of grid columns (width)
grid_height = 10  # Number of grid rows (height)
numMine = ""          # Number of mines (set later by user input)
grid_size = 32        # Size of each grid square in pixels
border = 16           # General border size (left, right, bottom)
top_border = 25      # Top border size for menu/spacing
app_width = grid_size * grid_width + border * 2  # App window width in pixels
app_height = grid_size * grid_height + border + top_border  # App window height in pixels

# Creates main pygame window
gameDisplay = pygame.display.set_mode((app_width, app_height))  
pygame.display.set_caption("Minesweeper")  # Set window title to "Minesweeper"

# ---------- Loads sprite images for game ----------
sprite_emptyGrid = pygame.image.load("Sprites/Grid_ClickedOn.png")  # Revealed empty grid
sprite_flag = pygame.image.load("Sprites/flag.png")                # Flag marker
sprite_grid = pygame.image.load("Sprites/Grid.png")                # Hidden grid square
sprite_grid1 = pygame.image.load("Sprites/gridnum1.png")           # Grid with number 1
sprite_grid2 = pygame.image.load("Sprites/gridnum2.png")           # Grid with number 2
sprite_grid3 = pygame.image.load("Sprites/gridnum3.png")           # Grid with number 3
sprite_grid4 = pygame.image.load("Sprites/gridnum4.png")           # Grid with number 4
sprite_grid5 = pygame.image.load("Sprites/gridnum5.png")           # Grid with number 5
sprite_grid6 = pygame.image.load("Sprites/gridnum6.png")           # Grid with number 6
sprite_grid7 = pygame.image.load("Sprites/gridnum7.png")           # Grid with number 7
sprite_grid8 = pygame.image.load("Sprites/gridnum8.png")           # Grid with number 8
sprite_mine = pygame.image.load("Sprites/mineNeutral.png")         # Untriggered mine
sprite_mineClicked = pygame.image.load("Sprites/mineClickedOn.png")# Mine that was clicked
sprite_mineFalse = pygame.image.load("Sprites/mineFalse.png")      # Wrongly flagged mine

# ---------- Utility function ----------
def drawText(txt, s, yOff=0):
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
    gameDisplay.blit(screen_text, rect)  # Draws text to screen

#Maybe add class object here for grid that draws grid and updates for every tile selected?
class Grid:
    def __init__(self, xGrid, yGrid, type):
        self.xGrid = xGrid
        self.yGrid = yGrid
        self.clicked = False
        self.mineClicked = False
        self.mineFalse = False
        self.flag = False
        #Rect(left, top, width, height) -> Rect
        self.rect = pygame.Rect(border + self.xGrid * grid_size,
                                top_border + self.yGrid * grid_size,
                                grid_size, grid_size)
        self.val = type

    #draws the sprites onto grid after every click/interaction update
    def drawGrid(self):
        if self.mineFalse:
            gameDisplay.blit(sprite_mineFalse, self.rect)
        else:
            if self.clicked:
                if self.val == "b":
                    if self.mineClicked:
                        gameDisplay.blit(sprite_mineClicked, self.rect)
                    else:
                        gameDisplay.blit(sprite_mine, self.rect)
                else:
                    if self.val == 0:
                        gameDisplay.blit(sprite_emptyGrid, self.rect)
                    elif self.val == 1:
                        gameDisplay.blit(sprite_grid1, self.rect)
                    elif self.val == 2:
                        gameDisplay.blit(sprite_grid2, self.rect)
                    elif self.val == 3:
                        gameDisplay.blit(sprite_grid3, self.rect)
                    elif self.val == 4:
                        gameDisplay.blit(sprite_grid4, self.rect)
                    elif self.val == 5:
                        gameDisplay.blit(sprite_grid5, self.rect)
                    elif self.val == 6:
                        gameDisplay.blit(sprite_grid6, self.rect)
                    elif self.val == 7:
                        gameDisplay.blit(sprite_grid7, self.rect)
                    elif self.val == 8:
                        gameDisplay.blit(sprite_grid8, self.rect)
            else:
                if self.flag:
                    gameDisplay.blit(sprite_flag, self.rect)
                else:
                    gameDisplay.blit(sprite_grid, self.rect)


# ---------- Game loop (to be implemented) ----------
bg_color = (192, 192, 192) # Background gray color
grid_color = (128, 128, 128) # Grid line gray color

def gameLoop(grid, mines):
    gameDisplay.fill((192, 192, 192))

    # Draw grid
    print("GameLoop grid")
    for row in grid:
        for cell in row:
            cell.drawGrid()

    pygame.display.update()
    pygame.time.delay(5000) # pauses for 5 seconds before closing to prevent auto closing since its not in a loop 
    pygame.quit()
    quit()


#-----------main_menu sys call ------------
if len(sys.argv) > 1:
    try:
        numMine = int(sys.argv[1])
        # ---------- Program entry point ----------
        print(f"gameloop start... \nNumber of Mines = {numMine}")  # Debug print to console

        # 1. Create bomb grid (10x10 with bombs randomly placed)
        raw_grid = BoardGenerator.generate_bombs(numMine)

        #-> Prints raw_grid
        print("Heres raw_grid:")
        BoardGenerator.print_grid(raw_grid)
    
        # 2. Convert raw grid into Grid objects
        grid = [[Grid(x, y, "b" if raw_grid[y][x] == 'b' else int(raw_grid[y][x])) for x in range(grid_width)] for y in range(grid_height)]
        mines = [(x, y) for y in range(grid_height) for x in range(grid_width) if raw_grid[y][x] == 'b']

        # 3. Starts gameloop with grid and mines objects
        gameLoop(grid, mines)  # Call main game loop if valid input in main menu entered
        
    except ValueError:
        numMine = 10  # fallback to 10 if bad input detected
        gameDisplay.fill((192, 192, 192))  # Shows clear screen with background gray
        drawText("Non-integer detected,", 30, -80)
        drawText("provide integer only input", 30, -40)
        pygame.display.update()
        pygame.time.delay(5000)  # pause for 5 seconds so user can read it

# ---------- Cleanup when program ends ----------
pygame.quit()  #Uninitializes all pygame modules
quit()  #Exits program