'''
A main menu for Minesweeper using Pygame.
Allows player to select the number of mines (10-20) and start the game.
Inputs: player chosen number of mines.
Outputs:
    running the actual game with the grid
    the number of mines will be sent to it.
Sources:
    Used Copilot to help spacing out the buttons.
    Pygame event handling documentation used in main_menu(): https://www.pygame.org/docs/ref/event.html
Author: Atharva Patil
Creation Date: 9/2/2025
'''

import pygame
import sys
import subprocess # to open MineSweeper.py and give it the mine count

pygame.init()

# screen setup
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper - Main Menu")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (50, 100, 200)

# fonts
FONT = pygame.font.SysFont(None, 36)
SMALL_FONT = pygame.font.SysFont(None, 28)

# menu state
mine_count = 10  # default

# buttons
start_button = pygame.Rect(WIDTH//2 - 60, HEIGHT - 80, 120, 40)
minus_button = pygame.Rect(WIDTH//2 - 70, HEIGHT//2 - 20, 40, 40)
plus_button = pygame.Rect(WIDTH//2 + 30, HEIGHT//2 - 20, 40, 40)

def draw_menu(): # draw how menu looks
    screen.fill(WHITE)

    # title
    title_text = FONT.render("Minesweeper", True, BLACK)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 30))

    # mine count label
    label_text = SMALL_FONT.render("Select Mine Count:", True, BLACK)
    screen.blit(label_text, (WIDTH//2 - label_text.get_width()//2, HEIGHT//2 - 60))

    # mine count display
    count_text = FONT.render(str(mine_count), True, BLUE)
    screen.blit(count_text, (WIDTH//2 - count_text.get_width()//2, HEIGHT//2))

    # minus button
    pygame.draw.rect(screen, GRAY, minus_button)
    minus_text = FONT.render("-", True, BLACK)
    screen.blit(minus_text, (minus_button.centerx - minus_text.get_width()//2, minus_button.centery - minus_text.get_height()//2))

    # plus button
    pygame.draw.rect(screen, GRAY, plus_button)
    plus_text = FONT.render("+", True, BLACK)
    screen.blit(plus_text, (plus_button.centerx - plus_text.get_width()//2, plus_button.centery - plus_text.get_height()//2))

    # start button
    pygame.draw.rect(screen, DARK_GRAY, start_button)
    start_text = SMALL_FONT.render("Start Game", True, WHITE)
    screen.blit(start_text, (start_button.centerx - start_text.get_width()//2, start_button.centery - start_text.get_height()//2))

    pygame.display.flip()

def main_menu(): # run main menu and handle events
    global mine_count
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # when button is clicked
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if minus_button.collidepoint(event.pos):
                    if mine_count > 10:
                        mine_count -= 1
                elif plus_button.collidepoint(event.pos):
                    if mine_count < 20:
                        mine_count += 1
                elif start_button.collidepoint(event.pos):
                    # run MineSweeper.py and pass mine_count so it can be used there
                    pygame.quit()
                    subprocess.run([sys.executable, "MineSweeper.py", str(mine_count)])
                    sys.exit()

        draw_menu()
        clock.tick(30)

if __name__ == "__main__":
    main_menu()

