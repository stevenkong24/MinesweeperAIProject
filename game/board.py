import random

import numpy as np
import game
import pygame

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

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != -1:
                surroundings = get_surroundings(i, j, grid)
                grid[i][j] = surroundings.count(-1)
    return grid

def generate_covered(n, m):
    grid = [["#"] * m for _ in range(n)]
    return grid

def random_coverage(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if random.randint(0, 2) == 1:
                grid[i][j] = -2
    return grid


def create_label_grid(grid):
    label_grid = [[0] * len(grid[0]) for _ in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == -1:
                label_grid[i][j] = 1
    return label_grid


def create_data(n, m, n_mines, amount):
    boards = []
    for i in range(amount):
        print(f'generated data point {i+1}/{amount}')
        grid = generate(n, m, n_mines)
        label_grid = create_label_grid(grid)
        grid = random_coverage(grid)

        grid = np.array(grid)
        grid = np.expand_dims(grid, axis=-1)
        grid = np.expand_dims(grid, axis=-0)
        label_grid = np.array(label_grid)
        label_grid = np.expand_dims(label_grid, axis=-1)
        label_grid = np.expand_dims(label_grid, axis=-0)

        boards.append([grid, label_grid])
    return boards

def get_dimensions(grid):
    return(len(grid), len(grid[0])) 

if __name__ == '__main__':
    # pygame.init()
    # screen = pygame.display.set_mode((800, 600))
    
    uncovered_grid = generate(30, 16, 1)
    cur_grid = generate_covered(30, 16)
    
    label_grid = create_label_grid(uncovered_grid)
    # grid = random_coverage(grid)
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
        decision = input("R to reveal square, F to flag square, C to clear squares around square: ")
        coords = input("X, Y coordinates of desired square: ")
        coords = tuple(map(int, coords.split(', ')))
        x, y = coords
        if (decision == 'R'):
            cur_grid = game.reveal_square(x, y, cur_grid, uncovered_grid)
        elif (decision == 'F'):
            cur_grid = game.flag_square(x, y, cur_grid)
        elif (decision == 'C'):
            cur_grid = game.clear_square(x, y, cur_grid, uncovered_grid)
        
        if cur_grid == False:
            break
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

        print(str(game.mines_remaining(cur_grid, uncovered_grid)) + " mines remaining")
        print()
        if game.mines_remaining(cur_grid, uncovered_grid) == 0:
            cur_grid = True
            break
        # screen.fill((0, 0, 255))
        # pygame.display.flip()
    if cur_grid:
        print("You won")
    else:
        print("You lost")
    
    