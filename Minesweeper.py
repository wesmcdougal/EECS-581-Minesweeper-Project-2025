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
top_border = 80      # Top border size for menu/spacing
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

        #flag to track first click 
        self.first_click = True

        # ---------- HUD Assets ----------
        self.flag_icon = pygame.image.load("sprites/flag.png")
        self.retry_icon = pygame.image.load("sprites/retry.png")
        self.quit_icon = pygame.image.load("sprites/quit.png")

        # Icons on HUD
        icon_size = 48
        self.flag_icon = pygame.transform.scale(self.flag_icon, (icon_size, icon_size))
        self.retry_icon = pygame.transform.scale(self.retry_icon, (icon_size, icon_size))
        self.quit_icon = pygame.transform.scale(self.quit_icon, (icon_size, icon_size))

        # Rects for interaction
        self.flag_rect = self.flag_icon.get_rect(topleft=(border, border))
        self.retry_rect = self.retry_icon.get_rect(topleft=(border + 120, border))
        self.quit_rect = self.quit_icon.get_rect(topleft=(border + 180, border))

        # Track game state text
        self.game_status = "Playing"
    
    def draw_hud(self, surface):
        # Draw flag icon + remaining flag count
        surface.blit(self.flag_icon, self.flag_rect.topleft)

        # Count how many flags are currently placed on the board
        flags_placed = sum(cell.flag for row in self.grid for cell in row)

        # Calculate remaining flags available to place
        remaining_flags = len(self.mines) - flags_placed

        font = pygame.font.SysFont("Calibri", 24, True)
        text = font.render(str(remaining_flags), True, black)
        surface.blit(text, (self.flag_rect.right + 15, self.flag_rect.y + 15))

        # Draw retry + quit buttons
        surface.blit(self.retry_icon, self.retry_rect.topleft)
        surface.blit(self.quit_icon, self.quit_rect.topleft)
        
        # Determine text color based on game status
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
        if self.game_status == "Playing":
            status_color = BLUE
        elif self.game_status == "Win":
            status_color = GREEN
        elif self.game_status == "Loss":
            status_color = RED

        # Draw game state (Playing, Win, Loss)
        status_text = font.render(self.game_status, True, status_color)
        surface.blit(status_text, (app_width - status_text.get_width() - border, border + 15))

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

                    #for debug purposes only!!!! press w to win
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:  # Press "W" to trigger a win
                            self.game_over = True
                            self.game_win = True
                            self.game_status = "Win"
                            # Optionally reveal all cells
                            for row in self.grid:
                                for cell in row:
                                    cell.clicked = True

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()

                        # HUD interactions first
                        if self.retry_rect.collidepoint(mouse_pos):
                            self.initialized = False  # reset
                            self.first_click = True
                            self.run()  # restart game
                            return
                        elif self.quit_rect.collidepoint(mouse_pos):
                            self.gameStateManager.setState("main_menu")
                            return
                        for row in self.grid:
                            for cell in row:
                                if cell.rect.collidepoint(mouse_pos): #If mouse click is within cell
                                    if event.button == 1:  #Left click
                                        if self.first_click:
                                            self.first_click = False
                                            result = cell.reveal()
                                            # If it's a mine, just reveal it but don't end the game
                                            if result == "mine":
                                                cell.mineClicked = True  # Optional: mark visually
                                                result = None  # Prevent game over
                                        else:
                                            result = cell.reveal()
                                            if result == "mine":
                                                # Game over: player clicked on a mine
                                                self.game_over = True
                                                self.game_win = False
                                                self.game_status = "Loss"
                                                # Reveal all mines
                                                for mx, my in self.mines:
                                                    self.grid[my][mx].clicked = True
                                        # If the cell is empty, recursively reveal neighbors
                                        if result == "empty":
                                            self.reveal_neighbors(cell.xGrid, cell.yGrid)

                                        # Check for win
                                        if self.check_win():
                                            self.game_over = True
                                            self.game_win = True
                                            self.game_status = "Win"
                                    elif event.button == 3:  #Right click
                                        cell.toggleFlag() #Place flag

                # Draw grid
                #Create off-screen frame buffer
                frame_surface = pygame.Surface((app_width, app_height))
                frame_surface.fill((192, 192, 192))  # background
                for row in self.grid:
                    for cell in row:
                        cell.drawGrid(frame_surface)

                self.draw_hud(frame_surface)
                #Blit buffer to main display
                self.gameDisplay.blit(frame_surface, (0,0))
                pygame.display.flip()  # flip once per frame
                self.clock.tick(30)

            # Wait for user input to restart or quit
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.retry_rect.collidepoint(mouse_pos):
                            self.initialized = False  # Reset
                            self.first_click = True
                            self.game_status = "Playing"
                            self.run()  # Restart game
                            waiting = False
                        elif self.quit_rect.collidepoint(mouse_pos):
                            self.gameStateManager.setState("main_menu")
                            waiting = False
    
    def reveal_neighbors(self, x, y):
        queue = [(x, y)]
        visited = set()
        
        while queue:
            cx, cy = queue.pop(0)  # Process current cell
            
            # Skip if already processed
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            
            # Check all 8 neighbors
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    # Skip the center cell (current cell)
                    if dx == 0 and dy == 0:
                        continue
                        
                    nx, ny = cx + dx, cy + dy
                    
                    # Check bounds and if already visited
                    if (0 <= nx < grid_width and 0 <= ny < grid_height and 
                        (nx, ny) not in visited):
                        
                        neighbor = self.grid[ny][nx]
                        
                        # Only reveal unclicked, unflagged cells
                        if not neighbor.clicked and not neighbor.flag:
                            result = neighbor.reveal()
                            
                            # If empty, add to queue for further processing
                            if result == "empty":
                                queue.append((nx, ny))

    def check_win(self):
        for row in self.grid:
            for cell in row:
                if cell.val != "b" and not cell.clicked:
                    return False
        return True
