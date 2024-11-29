import board
#game code
def reveal_square(x, y, cur_grid, uncovered_grid):
    size = board.get_dimensions(cur_grid)
    if (uncovered_grid[x][y] == -1):
        # return false if lose
        return False
    elif (uncovered_grid[x][y] > 0):
        cur_grid[x][y] = uncovered_grid[x][y]
        return cur_grid

    else:
        cur_grid[x][y] = uncovered_grid[x][y]
        toSearch = [(x, y)]
        while (toSearch):
            x, y = toSearch.pop(0)
            if (0 in board.get_surroundings(x, y, uncovered_grid)):
                for coord in board.surrounding_points(x, y):
                    x, y = coord
                    # print(x)
                    # print(y)
                    # if x < size[0] and y < size[1] and uncovered_grid[x][y] == 0 and cur_grid[x][y] == "#":
                    if x < size[0] and y < size[1] and uncovered_grid[x][y] != -1 and cur_grid[x][y] == "#" and 0 in board.get_surroundings(x, y, uncovered_grid):
                        cur_grid[x][y] = uncovered_grid[x][y]
                        toSearch.append((x, y))
                        
                    

        return cur_grid
        # print(board.get_surroundings(x, y, uncovered_grid))

def flag_square(x, y, cur_grid):
    if isinstance(cur_grid[x][y], str) and cur_grid[x][y] == "#":
        cur_grid[x][y] = "!"
    elif isinstance(cur_grid[x][y], str) and cur_grid[x][y] == "!":
        cur_grid[x][y] = "#"
    return cur_grid

def mines_remaining(cur_grid, uncovered_grid):
    return sum(element == -1 for row in uncovered_grid for element in row) - sum(element == '!' for row in cur_grid for element in row)

def clear_square(x, y, cur_grid, uncovered_grid):
    # Error here
    if (board.get_surroundings(x, y, cur_grid).count("!") == cur_grid[x][y]):
        # use surrounding points instead
        size = board.get_dimensions(cur_grid)
        
        print(board.get_surroundings(x, y, cur_grid))
        for coord in board.surrounding_points(x, y):
            print(coord)
            if x < size[0] and y < size[1]:
                coord_x, coord_y = coord
                if (cur_grid[coord_x][coord_y] != "!"):
                    cur_grid = reveal_square(coord_x, coord_y, cur_grid, uncovered_grid)
                    
                    if not cur_grid:
                        return False

        '''
        if (0 in board.get_surroundings(x, y, uncovered_grid)):
                for coord in board.surrounding_points(x, y):
                    x, y = coord
                    # print(x)
                    # print(y)
                    # if x < size[0] and y < size[1] and uncovered_grid[x][y] == 0 and cur_grid[x][y] == "#":
                    if x < size[0] and y < size[1] and uncovered_grid[x][y] != -1 and cur_grid[x][y] == "#" and 0 in board.get_surroundings(x, y, uncovered_grid):
                        cur_grid[x][y] = uncovered_grid[x][y]
                        toSearch.append((x, y))
                        
        '''
    return cur_grid