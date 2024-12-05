import board
#game code
def reveal_square(y, x, cur_grid, uncovered_grid):
    size = board.get_dimensions(cur_grid)
    if (uncovered_grid[y][x] == -1):
        # return false if lose
        return False
    elif (uncovered_grid[y][x] > 0):
        cur_grid[y][x] = uncovered_grid[y][x]
        return cur_grid

    else:
        cur_grid[y][x] = uncovered_grid[y][x]
        toSearch = [(y, x)]
        while (toSearch):
            y, x = toSearch.pop(0)
            # if (uncovered_grid[y][x])
            
            if (0 in board.get_surroundings(y, x, uncovered_grid)):
                for coord in board.surrounding_points(y, x):
                    
                    
                    new_y, new_x = coord
                    # print(x)
                    # print(y)
                    # if x < size[0] and y < size[1] and uncovered_grid[x][y] == 0 and cur_grid[x][y] == "#":
                    if new_y < size[0] and new_x < size[1] and uncovered_grid[new_y][new_x] != -1 and cur_grid[new_y][new_x] == "#":
                        cur_grid[new_y][new_x] = uncovered_grid[new_y][new_x]
                        if (uncovered_grid[new_y][new_x] == 0):
                            toSearch.append((new_y, new_x))                

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
            coord_x, coord_y = coord
            if coord_x < size[0] and coord_y < size[1]:
                
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

def check_if_correct(cur_grid, uncovered_grid):
    for i in range(len(cur_grid)):
        for j in range(len(cur_grid[0])):
            if cur_grid[i][j] == "!" and uncovered_grid[i][j] != -1:
                return False
    return True