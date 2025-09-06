import random
#----------print grid(for debuging)
def print_grid(grid):
    for i in grid:
        print(i)

# ---------Generate Bombs----------
def generate_bombs(bombCount):
    #create 10 by 10 grid
    grid = [[0 for _ in range(10)] for _ in range(10)]
    
    #place bombs at random location on grid
    i = 0
    while i < bombCount:
        placement = random.randint(0,99)
        row = placement//10
        column = placement%10
        
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
                #check suroundings
                pass


def generate_statusGrid(grid):
    pass


grid = generate_bombs(10)
print_grid(grid)