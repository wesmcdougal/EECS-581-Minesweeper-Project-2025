# how to install pygames - https://www.geeksforgeeks.org/installation-guide/how-to-install-pygame-in-windows/
# Pygames documentation - https://www.pygame.org/docs/
#                         https://coderslegacy.com/python/python-pygame-tutorial/

import pygame  # Imports pygame library
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
top_border = 100      # Top border size for menu/spacing
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

# ---------- Main Menu ----------
def main_menu():
    """
    Displays the main menu where the player enters number of mines.
    Returns True if valid input is entered (start game), otherwise False.
    """
    global numMine  # global variable numMine
    grey = (48,49,52,255)
    gameDisplay.fill(grey)
    main_menu_bg = pygame.image.load("Sprites/main_menu_bg.png")  # Loads menu background image
    input_box = pygame.Rect(app_width / 2 - 25, app_height / 2 - 100, 140, 32)  # Input box rectangle
    color_inactive = pygame.Color('lightskyblue3')  # Color when input inactive
    color_active = pygame.Color('dodgerblue2')      # Color when input active
    color = color_inactive  # Start inactive
    active = False          # Input box is initially inactive
    mine_input_text = str(numMine)  # Input text string for number of mines
    font = pygame.font.Font(None, 32)  # Font object for rendering input text
    
    # ----- Menu loop -----
    menu_running = True
    while menu_running:
        for event in pygame.event.get():  # Process all events
            if event.type == pygame.QUIT:  # If user closes window
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # If mouse is clicked
                if input_box.collidepoint(event.pos):  # Check if click inside input box
                    active = not active  # Toggle active state
                else:
                    active = False  # Otherwise deactivate state
                color = color_active if active else color_inactive  # Changes box color
            if event.type == pygame.KEYDOWN:  # If a key is pressed
                if active:  # Only process input if input box is currently active
                    if event.key == pygame.K_RETURN:  # Enter key pressed
                        try:
                            new_num_mines = int(mine_input_text)  # Converts input to integer
                            if new_num_mines >= 1 and new_num_mines < 100:
                                numMine = new_num_mines  # Save number of mines
                                return True  # Exit menu and start game
                            else:
                                mine_input_text = ""  # Clear invalid input
                        except ValueError:  # If input was not a number
                            mine_input_text = ""  # Clear invalid input
                    elif event.key == pygame.K_BACKSPACE:  # Backspace pressed
                        mine_input_text = mine_input_text[:-1]  # Removes last character
                    else:
                        mine_input_text += event.unicode  # Append typed character to input
        
        # Scale the menu background image
        menu_bg = pygame.transform.scale(main_menu_bg, (app_width - 50, app_height - 50))

        # Get the rect of the scaled image
        menu_bg_rect = menu_bg.get_rect()

        # Center the rect on the screen
        menu_bg_rect.center = (app_width // 2, app_height // 2)

        # Draw the image at its centered position
        gameDisplay.blit(menu_bg, menu_bg_rect)
        
        # Draw menu text
        drawText("Minesweeper", 50, app_height / 10 - 250)  # Title text
        drawText("Enter number of mines:", 30, app_height / 5 - 250)  # Instructions
        
        # Render the input box with current text
        txt_surface = font.render(mine_input_text, True, white)  #input text
        width = max(50, txt_surface.get_width())  #Adjust box width based on text length
        input_box.w = width  #Update input box width
        gameDisplay.blit(txt_surface, (input_box.x + 5, input_box.y + 5))  #Draw text inside box
        pygame.draw.rect(gameDisplay, color, input_box, 2)  #Draw input box outline
        pygame.display.update()  # Refresh screen
    
    return False  # If menu exits without valid input


#Maybe add class object here for grid that draws grid and updates for every tile selected?


# ---------- Game loop (to be implemented) ----------
bg_color = (192, 192, 192) # Background gray color
grid_color = (128, 128, 128) # Grid line gray color
def gameLoop():
    pass

# ---------- Program entry point ----------
if main_menu():  # Start with main menu
    print(f"gameloop start... \nNumber of Mines = {numMine}")  # Debug print to console
    gameLoop()  # Call main game loop if valid input in main menu entered

# ---------- Cleanup when program ends ----------
pygame.quit()  #Uninitializes all pygame modules
quit()  #Exits program
