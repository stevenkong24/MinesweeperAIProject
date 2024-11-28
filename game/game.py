import board
#game code
def revealSquare(curr_grid, uncovered_grid, coord):
    x, y = coord
    if (uncovered_grid[x][y] == -1):
        # return false if lose
        return False
    elif (uncovered_grid[x][y] > 0):
        curr_grid[x][y] = uncovered_grid[x][y]
        return curr_grid
    else:
        print(uncovered_grid[x][y])
    