'''
File for grid object and sprite loading
'''

import pygame

# Loads sprite images for game
sprite_emptyGrid = pygame.image.load("Sprites/Grid_ClickedOn.png")  # Revealed empty grid
sprite_flag = pygame.image.load("Sprites/flag.png")                 # Flag marker
sprite_grid = pygame.image.load("Sprites/Grid.png")                 # Hidden grid square
sprite_grid1 = pygame.image.load("Sprites/gridnum1.png")            # Grid with number 1
sprite_grid2 = pygame.image.load("Sprites/gridnum2.png")            # Grid with number 2
sprite_grid3 = pygame.image.load("Sprites/gridnum3.png")            # Grid with number 3
sprite_grid4 = pygame.image.load("Sprites/gridnum4.png")            # Grid with number 4
sprite_grid5 = pygame.image.load("Sprites/gridnum5.png")            # Grid with number 5
sprite_grid6 = pygame.image.load("Sprites/gridnum6.png")            # Grid with number 6
sprite_grid7 = pygame.image.load("Sprites/gridnum7.png")            # Grid with number 7
sprite_grid8 = pygame.image.load("Sprites/gridnum8.png")            # Grid with number 8
sprite_mine = pygame.image.load("Sprites/mineNeutral.png")          # Untriggered mine
sprite_mineClicked = pygame.image.load("Sprites/mineClickedOn.png") # Mine that was clicked
sprite_mineFalse = pygame.image.load("Sprites/mineFalse.png")       # Wrongly flagged mine


# Grid class to represent each cell in the minesweeper grid
class Grid:
    def __init__(self, xGrid, yGrid, type, gameDisplay, border, top_border, grid_size,):

        self.xGrid = xGrid
        self.yGrid = yGrid
        self.clicked = False
        self.mineClicked = False
        self.mineFalse = False
        self.flag = False
        self.rect = pygame.Rect(border + self.xGrid * grid_size,
                                top_border + self.yGrid * grid_size,
                                grid_size, grid_size)
        self.val = type
        self.gameDisplay = gameDisplay

    # Function for drawing the sprites onto grid after every click/interaction update
    def drawGrid(self, surface):
        if self.mineFalse:
            surface.blit(sprite_mineFalse, self.rect)

        else:
            if self.clicked:
                if self.val == "b": # If the clicked grid is a mine
                    if self.mineClicked:
                        surface.blit(sprite_mineClicked, self.rect)
                    else:
                        surface.blit(sprite_mine, self.rect)

                else: # If the clicked grid is not a mine
                    if self.val == 0:
                        surface.blit(sprite_emptyGrid, self.rect)
                    elif self.val == 1:
                        surface.blit(sprite_grid1, self.rect)
                    elif self.val == 2:
                        surface.blit(sprite_grid2, self.rect)
                    elif self.val == 3:
                        surface.blit(sprite_grid3, self.rect)
                    elif self.val == 4:
                        surface.blit(sprite_grid4, self.rect)
                    elif self.val == 5:
                        surface.blit(sprite_grid5, self.rect)
                    elif self.val == 6:
                        surface.blit(sprite_grid6, self.rect)
                    elif self.val == 7:
                        surface.blit(sprite_grid7, self.rect)
                    elif self.val == 8:
                        surface.blit(sprite_grid8, self.rect)

            else: # If the grid is not clicked
                if self.flag:
                    surface.blit(sprite_flag, self.rect)
                else:
                    surface.blit(sprite_grid, self.rect)

    # Add flag toggle method           
    def toggleFlag(self): 
       if not self.clicked:
           self.flag = not self.flag

    # Add reveal method
    def reveal(self):
        if self.clicked or self.flag: # Reveal this tile and return its type
            return None  # Do nothing if already clicked or flagged
        self.clicked = True
        
        # Return the type of the grid
        if self.val == "b":
            self.mineClicked = True
            return "mine"
        elif self.val == 0:
            return "empty"
        else:
            return "number"
