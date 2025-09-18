'''
File for generating the board, bombs, and mine proximity cell value for minesweeper
'''

import random

# Print grid (for debugging purposes)
def print_grid(grid):
    for i in grid:
        print(i)


# Generate Bombs
def generate_bombs(bombCount):

    grid = [[0 for _ in range(10)] for _ in range(10)] # Create 10 by 10 grid
    
    # Place bombs at random location on grid
    i = 0
    while i < bombCount: 
        placement = random.randint(0,99)
        row = placement//10
        column = placement%10

        # If current placement is not a bomb, proceed with placement
        if grid[row][column] != 'b':
            grid[row][column] = 'b'
            i+=1

    return grid


# Generate the numbers proximal to mines
def generate_numbering(grid):

    # Iterate through entire grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):

            if grid[i][j] == 'b': # If a bomb cell is found
                for di in [-1, 0, 1]: # Check all 8 surrounding cells
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0: # Skip the bomb cell itself
                            continue
                        
                        # Calculate adjacent cell coordinates
                        ni, nj = i + di, j + dj
                        
                        # Check if coordinates are within grid bounds
                        if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
                            # Only increment if the adjacent cell is not a bomb
                            if grid[ni][nj] != 'b':
                                grid[ni][nj] += 1
    return grid

# print_grid(grid)
