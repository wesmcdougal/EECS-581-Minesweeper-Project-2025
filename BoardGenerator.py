import random
#----------print grid(for debuging)
def print_grid(grid):
    for i in grid:
        print(i)

# ---------Generate Bombs----------
def generate_bombs(bombCount, safe_row=None, safe_col=None):
    #create 10 by 10 grid
    grid = [[0 for _ in range(10)] for _ in range(10)]
    
    #place bombs at random location on grid
    i = 0
    while i < bombCount:
        placement = random.randint(0,99)
        row = placement//10
        column = placement%10

        #if a safe row and col are specified all blocks within a one block radius should be safe from bombs
        if safe_row and safe_col:
            if abs(row - safe_row) <= 1 and abs(column - safe_col) <= 1:
                continue

        #if current placement is not a bomb
        if grid[row][column] != 'b':
            grid[row][column] = 'b'
            i+=1

    return grid

#-------generate the numbers that
def generate_numbering(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'b':
                # Check all 8 surrounding cells
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        # Skip the bomb cell itself
                        if di == 0 and dj == 0:
                            continue
                        
                        # Calculate adjacent cell coordinates
                        ni, nj = i + di, j + dj
                        
                        # Check if coordinates are within grid bounds
                        if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
                            # Only increment if the adjacent cell is not a bomb
                            if grid[ni][nj] != 'b':
                                grid[ni][nj] += 1
    return grid