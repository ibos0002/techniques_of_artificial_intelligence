from NRP import Puzzle, Puzzle_solution

import heapq
from typing import Optional

def manhattan_heuristic(p: Puzzle):
    # Returns the average manhattan distance of each number in a given puzzle to its
    # position in the solved configuration
    #   p:  NRP of class Puzzle

    h = 0
    n = p.width*p.height
    for y in range(p.height):
        for x in range(p.width):
            current_number = p.configuration[y][x]
            if current_number is None:
                continue
            solved_y = (current_number-1)//p.width
            solved_x = current_number-1 - solved_y*p.width
            h += abs(solved_x-x) + abs(solved_y-y)

    return h/n

def rotation_neighbours(p: Puzzle, rows: list[int], cols: list[int]):
    # Returns a list of puzzles with a configuration that can be reached from a given puzzle
    # by rotating a single 2x2 square block clockwise
    #   p:  NRP of class Puzzle
    #   rows:   index of rows that need to be solved
    #   cols:   index of columns that need to be solved

    neigh_list = []
    if len(rows) == 0:
        min_row = 0
    else:
        min_row = min(rows)

    if len(cols) == 0:
        min_col = 0
    else:
        min_col = min(cols)

    for y in range(min_row,p.height-1):
        for x in range(min_col,p.width-1):
            if any([p.configuration[r][c] is not None for r in [y,y+1] for c in [x,x+1]]):
                neigh_list.append((p.rotate(x,y),(x,y)))
    return neigh_list

def solved(p: Puzzle, goal: Puzzle, rows: list[int], cols: list[int]):
    if len(rows) == 0:
        min_row = 0
    else:
        min_row = min(rows)

    if len(cols) == 0:
        min_col = 0
    else:
        min_col = min(cols)

    for y in range(min_row,p.height):
        for x in range(min_col,p.width):
            if y in rows or x in cols:
                if p.configuration[y][x] != goal.configuration[y][x]:
                    return False
    return True

def start_puzzle(p: Puzzle, goal: Puzzle, rows: list[int], cols: list[int]):
    indices = []

    if len(rows) == 0:
        min_row = 0
    else:
        min_row = min(rows)

    if len(cols) == 0:
        min_col = 0
    else:
        min_col = min(cols)

    for y in range(min_row,goal.height):
        for x in range(min_col,goal.width):
            if (y in rows) or (x in cols):
                goal_value = goal.configuration[y][x]
                for j in range(p.height):
                    for i in range(p.width):
                        if p.configuration[j][i] == goal_value:
                            indices.append((i,j))

    start_config = []
    for y in range(p.height):
        temp_row = []
        for x in range(p.width):
            if (x,y) in indices:
                temp_row.append(p.configuration[y][x])
            else:
                temp_row.append(None)
        start_config.append(temp_row)

    return Puzzle(p.width,p.height,start_config)


def A_star(p: Puzzle, rows: Optional[list[int]] = None, cols: Optional[list[int]] = None):
    # Run an A* search to solve the given NRP using as a heuristic the average manhattan
    # distance and as cost the number of moves done
    #   start:  NRP of class Puzzle
    #   rows:   index of rows that need to be solved
    #   cols:   index of columns that need to be solved

    if rows is None:
        rows = range(p.height)
    if cols is None:
        cols = range(p.width)

    goal = Puzzle(p.width,p.height)
    start = start_puzzle(p,goal,rows,cols)

    q = [(0,start,[])]
    heapq.heapify(q)

    g_scores = {start: 0}
    while len(q) != 0:
        current = heapq.heappop(q)
        if solved(current[1],goal,rows,cols):
            return current[2]

        for p,rotation in rotation_neighbours(current[1],rows,cols):
            g = g_scores[current[1]]+1
            f = g + manhattan_heuristic(p)
            if p not in g_scores or g < g_scores[p]:
                heapq.heappush(q,(f,p,current[2]+[rotation]))
                g_scores[p] = g

def search_runner(p: Puzzle, a_star: bool = False):
    # Function which splits the puzzle into regions and solves the regions one after another
    #   p:          NRP of class Puzzle
    #   a_star:     Boolean parameter which indicates whether to solve the entire puzzle at once
    #               with the A_star algorithm. Default value is False.

    if a_star:
        steps = A_star(p)
        return Puzzle_solution(p,steps)

    steps = []
    real_size = [p.height,p.width]
    current_puzzle = p
    current_size = [p.height,p.width]
    while current_size[0] > 3 and current_size[1] > 3:
        if current_size[0] == 3:
            cols = range(real_size[1]-current_size[1],real_size[1]-3)
            rows = []
            current_size[1] = 3
        else:
            if current_size[1] == 3:
                rows = range(real_size[0]-current_size[0],real_size[0]-3)
                cols = []
                current_size[0] = 3
            else:
                if current_size[0] == 4 and current_size[1] == 4:
                    rows = [real_size[0]-current_size[0]]
                    cols = [real_size[1]-current_size[1]]
                    current_size[0] -= 1
                    current_size[1] -= 1
                else:
                    if current_size[0] > current_size[1]:
                        rows = [real_size[0]-current_size[0]]
                        cols = []
                        current_size[0] -= 1
                    else:
                        rows = []
                        cols = [real_size[1]-current_size[1]]
                        current_size[1] -= 1

        current_steps = A_star(current_puzzle,rows,cols)
        steps.extend(current_steps)
        for rot in current_steps:
            current_puzzle = current_puzzle.rotate(rot[0],rot[1])

    rows = range(real_size[0]-current_size[0],real_size[0])
    cols = range(real_size[1]-current_size[1],real_size[1])
    current_steps = A_star(current_puzzle,rows,cols)
    steps.extend(current_steps)

    return Puzzle_solution(p,steps)
