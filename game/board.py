import random

import numpy as np
import pygame


def reveal_square(x, y, cur_grid, uncovered_grid):
    size = get_dimensions(cur_grid)
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
            if (0 in get_surroundings(x, y, uncovered_grid)):
                for coord in surrounding_points(x, y):
                    x, y = coord
                    # print(x)
                    # print(y)
                    # if x < size[0] and y < size[1] and uncovered_grid[x][y] == 0 and cur_grid[x][y] == "#":
                    if x < size[0] and y < size[1] and uncovered_grid[x][y] != -1 and cur_grid[x][
                        y] == "#" and 0 in get_surroundings(x, y, uncovered_grid):
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
    return sum(element == -1 for row in uncovered_grid for element in row) - sum(
        element == '!' for row in cur_grid for element in row)


def clear_square(x, y, cur_grid, uncovered_grid):
    # Error here
    if (get_surroundings(x, y, cur_grid).count("!") == cur_grid[x][y]):
        # use surrounding points instead
        size = get_dimensions(cur_grid)

        print(get_surroundings(x, y, cur_grid))
        for coord in surrounding_points(x, y):
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

MINE_CONST = 100
COVERED_CONST = -1
def generateForData(n, m, n_mines):
    grid = [[0] * m for _ in range(n)]
    mines = set()
    while len(mines) < n_mines:
        y = random.randint(0, n - 1)
        x = random.randint(0, m - 1)
        if (y, x) not in mines:
            mines.add((y, x))
            grid[y][x] = MINE_CONST #-1
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != MINE_CONST:
                surroundings = get_surroundings(i, j, grid)
                grid[i][j] = surroundings.count(MINE_CONST)
    return grid

def surrounding_points(x, y):
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1),
            (x - 1, y + 1)]


def get_surroundings(x, y, grid):
    values = []
    for point in surrounding_points(x, y):
        if point[0] >= 0 and point[1] >= 0:
            try:
                values.append(grid[point[0]][point[1]])
            except IndexError:
                continue
    return values


def generate(n, m, n_mines):
    grid = [[0] * m for _ in range(n)]
    mines = set()
    while len(mines) < n_mines:
        y = random.randint(0, n - 1)
        x = random.randint(0, m - 1)
        if (y, x) not in mines:
            mines.add((y, x))
            grid[y][x] = -1
    print(len(grid))
    print(len(grid[0]))
    rect = pygame.Rect(10, 10, cell_size * columns, cell_size * rows)
    # pygame.draw.rect(screen, (211, 211, 211), rect)
    pygame.draw.rect(screen, (220, 220, 220), rect)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            rect = pygame.Rect(10 + i * cell_size, 10 + j * cell_size, cell_size + 1, cell_size + 1)
            # pygame.draw.rect(screen, (211, 211, 211), rect)
            pygame.draw.rect(screen, (50, 50, 50), rect, 1)
            # pygame.draw.rect(screen, GRAY, rect, 1)  # Draw grid cell with a thin border
            
            if grid[i][j] != -1:
                surroundings = get_surroundings(i, j, grid)
                grid[i][j] = surroundings.count(-1)
    pygame.display.flip()
    return grid

def generate_covered(n, m):
    grid = [["#"] * m for _ in range(n)]
    return grid

def random_coverage(grid):
    covered_grid = generate_covered(len(grid), len(grid[0]))
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != MINE_CONST:
                if random.randint(0, 5) in [1, 2, 3]:
                    covered_grid = reveal_square(i, j, covered_grid, grid)
            else:
                if random.randint(0, 5) in [1]:
                    covered_grid[i][j] = MINE_CONST
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if covered_grid[i][j] == '#':
                covered_grid[i][j] = COVERED_CONST
    return covered_grid


def create_label_grid(grid):
    label_grid = [[0] * len(grid[0]) for _ in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == MINE_CONST:
                label_grid[i][j] = 1
    return label_grid

def create_coverage_mask(covered_grid):
    new_covered_grid = covered_grid.copy()
    for i in range(len(covered_grid)):
        for j in range(len(covered_grid[0])):
            if covered_grid[i][j] == COVERED_CONST:
                new_covered_grid[i][j] = 1
            else:
                new_covered_grid[i][j] = 0
    return new_covered_grid

def create_data(n, m, n_mines, amount):
    boards = []
    for i in range(amount):
        print(f'generated data point {i+1}/{amount}')
        grid = generateForData(n, m, n_mines)
        # for r in grid:
        #     frmt = "{:>3}" * len(r)
        #     print(frmt.format(*r))
        # print('\n-----------------------------------------\n')
        label_grid = create_label_grid(grid)
        grid = random_coverage(grid)
        # for r in grid:
        #     frmt = "{:>3}" * len(r)
        #     print(frmt.format(*r))
        # print('\n-----------------------------------------\n')
        coverage_map = create_coverage_mask(grid)
        # for r in coverage_map:
        #     frmt = "{:>3}" * len(r)
        #     print(frmt.format(*r))
        # print('\n-----------------------------------------\n')
        grid = np.array(grid)
        grid = np.expand_dims(grid, axis=-1)
        grid = np.expand_dims(grid, axis=-0)
        #print(grid)
        label_grid = np.array(label_grid)
        label_grid = np.expand_dims(label_grid, axis=-1)
        label_grid = np.expand_dims(label_grid, axis=-0)
        #print(label_grid)
        coverage_map= np.array(coverage_map)
        coverage_map = np.expand_dims(coverage_map, axis=-1)
        coverage_map = np.expand_dims(coverage_map, axis=-0)
        #print(coverage_map)

        boards.append([grid, label_grid, coverage_map])
    return boards

def set_dimensions(matrix):
    matrix = np.array(matrix)
    matrix = np.expand_dims(matrix, axis=-1)
    matrix = np.expand_dims(matrix, axis=-0)
    return matrix

def get_dimensions(grid):
    return(len(grid), len(grid[0])) 

def update_board(cur_grid):
    print(cur_grid)
    for i in range(len(cur_grid)):
        for j in range(len(cur_grid[0])):
            
            rect = pygame.Rect(10 + i * cell_size, 10 + j * cell_size, cell_size + 1, cell_size + 1)
            # pygame.draw.rect(screen, (211, 211, 211), rect)
            if (cur_grid[i][j] == '#'):
                pygame.draw.rect(screen, (220, 220, 220), rect)
            elif (cur_grid[i][j] == 0):
                pygame.draw.rect(screen, (255, 255, 255), rect)
            elif (cur_grid[i][j] == '!'):
                pygame.draw.rect(screen, (255, 0, 0), rect)
            else:
                # Fix this
                # screen.blit(my_font.render(str(game.mines_remaining(cur_grid, uncovered_grid)), False, (0, 0, 0)), (i * cell_size + 15, j * cell_size)) 
                print(get_surroundings(i, j, uncovered_grid))
                pygame.draw.rect(screen, (255, 255, 255), rect)
                screen.blit(my_font.render(str(get_surroundings(i, j, uncovered_grid).count(-1)), False, (0, 0, 0)), (i * cell_size + 15, j * cell_size))    
                
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
            # pygame.draw.rect(screen, GRAY, rect, 1)  # Draw grid cell with a thin border
    pygame.display.flip()


if __name__ == '__main__':
    rows = 16
    columns = 30
    mines = 99
    height = 600
    width = 1000
    cell_size = (width - 200) / columns
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill((255, 255, 255))
    pygame.font.init() 
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    
    uncovered_grid = generate(columns, rows, mines)
    cur_grid = generate_covered(columns, rows)
    label_grid = create_label_grid(uncovered_grid)
    # grid = random_coverage(grid)
    
    
    
    screen.blit(my_font.render(str(mines_remaining(cur_grid, uncovered_grid)) + " left", False, (0, 0, 0)), ((columns + 1) * cell_size, 0))
    pygame.display.flip()
    
    for r in uncovered_grid:
        frmt = "{:>3}" * len(r)
        print(frmt.format(*r))
    
    print()
    print("   0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5")
    print()
    count = 0
    for r in cur_grid:
        frmt = "{:>3}" * len(r)
        if count < 10:
            print(" " + str(count) + frmt.format(*r))
        else:
            print(str(count) + frmt.format(*r))
        count += 1
    
    print()
    x = 10
    y = 5
    # cur_grid = game.reveal_square(x, y, cur_grid, grid)
    #cur_grid = game.flagSquare(0, 5, cur_grid)
    
    while isinstance(cur_grid, list):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.fill((255, 255, 255))

                x, y = pygame.mouse.get_pos()
                # rint(width//)
                
                row = int((y - 10) // cell_size)
                col = int((x - 10) // cell_size)
                if row > rows or row < 0 or col > columns or columns < 0:
                    break
                
                if event.button == 1:
                    if cur_grid[col][row] == '#':
                        cur_grid = reveal_square(col, row, cur_grid, uncovered_grid)
                    else:
                        cur_grid = clear_square(col, row, cur_grid, uncovered_grid)

                elif event.button == 3:
                    cur_grid = flag_square(col, row, cur_grid)
               
                
                if cur_grid == False:
                    break

                update_board(cur_grid)

                print()
                print("    0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5")
                print()
                
                count = 0
                for r in cur_grid:
                    frmt = "{:>3}" * len(r)
                    if count < 10:
                        print(" " + str(count) + frmt.format(*r))
                    else:
                        print(str(count) + frmt.format(*r))
                    count += 1

                print(str(mines_remaining(cur_grid, uncovered_grid)) + " mines remaining")
                
                rect = pygame.Rect(10 + columns * cell_size, 0, cell_size + 1, cell_size + 1)
                # pygame.draw.rect(screen, (211, 211, 211), rect)
                pygame.draw.rect(screen, (255, 255, 255), rect)
                #pygame.display.update(pygame.Rect((columns + 1)* cell_size, 0, 100, 100))
                screen.blit(my_font.render(str(mines_remaining(cur_grid, uncovered_grid)) + " left", False, (0, 0, 0)), ((columns + 1) * cell_size, 0))
                print()
                if mines_remaining(cur_grid, uncovered_grid) == 0 and check_if_correct(cur_grid, uncovered_grid):
                    cur_grid = True
                    break
                # screen.fill((0, 0, 255))
                pygame.display.flip()
    if cur_grid:
        print("You won")
    else:
        print("You lost")
    
    