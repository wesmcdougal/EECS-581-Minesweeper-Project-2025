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
border = 30          # General border size (left, right, bottom)
top_border = 90      # Top border size for menu/spacing
grid_offset_x = 5  # move the grid placement x-axis 0 means center on x axis
grid_offset_y = 10  # move the grid placement y-axis 0 means center on y axis
app_width = grid_size * grid_width + border * 2  # App window width in pixels
app_height = grid_size * grid_height + border + top_border  # App window height in pixels

# ---------- Game loop (to be implemented) ----------
bg_color = (192, 192, 192) # Background gray color
grid_color = (128, 128, 128) # Grid line gray color

class MineSweeper:
    def __init__(self, gameStateManager):
        '''
        Takes in a gameStateManagers object and inializes the window that the board
        which the board will be drawn on
        '''
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
        self.flag_rect = self.flag_icon.get_rect(topleft=(border, border-20))
        self.retry_rect = self.retry_icon.get_rect(topleft=(border + 120, border-20))
        self.quit_rect = self.quit_icon.get_rect(topleft=(border + 180, border-20))

        # Track game state text
        self.game_status = "Playing"
    
    def draw_hud(self, surface):
        '''
        Draws the hud elements flags left, retry, back to menu, 
        and game status to the top of the provided surface
        '''
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
        surface.blit(status_text, (app_width - status_text.get_width() - border, border - 10))

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

    def draw_labels(self, surface):
        '''
        Draws column letters (A-J) and row numbers (1-10) around the grid
        '''
        font = pygame.font.SysFont("Calibri", 20, True)
        padding = 25
        #Create th txt for column
        for col in range(grid_width):
            # increment the column letter decimal value by 1 
            label = chr(ord('A') + col) 
            text = font.render(label, True, black)


            x = border + grid_offset_x + col * grid_size + grid_size // 2 - text.get_width() // 2
            #position on top of the grid
            y = top_border + grid_offset_y - 30
            surface.blit(text, (x, y))#draw too screen

        #Create th txt for row
        for row in range(grid_height):
            label = str(row + 1)
            text = font.render(label, True, black)
            #position to the left
            x = border + grid_offset_x - padding
            y = top_border + grid_offset_y + row * grid_size + grid_size // 2 - text.get_height() // 2
            surface.blit(text, (x, y))#draw too screen
    
    def initialize_minesweeper(self, safe_row=None, safe_col=None):
        '''
        Takes in safe_row and safe_col (both optional) that should be garanted to be empty
        and generated a grid will the specified amount of bombs. It then numbers the approximate
        mine count and converts the grid into sprite objects.
        '''
        # get number of mines from state manager
        params = self.gameStateManager.getParams()
        #set to 10 if param set to num
        numMine = params.get("numMine", 10)

        # ---------- Program entry point ----------
        #print(f"gameloop start... \nNumber of Mines = {numMine}")  # Debug print to console

        # 1. Create bomb grid (10x10 with bombs randomly placed)
        raw_grid = BoardGenerator.generate_bombs(numMine, safe_row, safe_col)
        #2. Create numbering for adjacent mines
        raw_grid = BoardGenerator.generate_numbering(raw_grid)

        # #-> Prints raw_grid
        # print("Heres raw_grid:")
        # BoardGenerator.print_grid(raw_grid)
    
        # 2. Convert raw grid into Grid objects
        self.grid = [[Grid(x, y, "b" if raw_grid[y][x] == 'b' else int(raw_grid[y][x]), self.gameDisplay, border+grid_offset_x, top_border+grid_offset_y, grid_size) for x in range(grid_width)] for y in range(grid_height)]
        self.mines = [(x, y) for y in range(grid_height) for x in range(grid_width) if raw_grid[y][x] == 'b']

        self.game_win = False
        self.game_over = False
        
        self.initialized = True


    def run(self):
            '''
            Initializes the board and handls player input (clicks, flags, quits), 
            updats the grid, checks win/loss conditions, and redraws the screen each frame
            '''
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
                                            if result != "empty":
                                                #regenerate and make clicked area safe
                                                self.initialize_minesweeper(cell.yGrid, cell.xGrid)
                                                self.grid[cell.yGrid][cell.xGrid].clicked = True
                                                if self.grid[cell.yGrid][cell.xGrid]:
                                                    self.reveal_neighbors(cell.xGrid, cell.yGrid)
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
               
                self.draw_labels(frame_surface)                

                self.draw_hud(frame_surface)
                #Blit buffer to main display
                self.gameDisplay.blit(frame_surface, (0,0))
                pygame.display.flip()  # flip once per frame
                self.clock.tick(30)

            # Wait for user input to restart or quit to menu
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
        '''
        Goes through the board and reveals empty
        spaces attached to a clicked empty space
        '''
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
        '''
        Iterate through the grid and checks if a 
        cell is not a bomb and has not been clicked.
        '''
        for row in self.grid:
            for cell in row:
                if cell.val != "b" and not cell.clicked:
                    return False
        return True
