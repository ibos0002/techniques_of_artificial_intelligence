from Project.NRP import Puzzle, solved_puzzle

import heapq

def manhattan_heuristic(p: Puzzle):
    # Returns the average manhattan distance of each number in a given puzzle to its
    # position in the solved configuration
    #   p:  NRP of class Puzzle

    h = 0
    n = p.width*p.height
    for y in range(p.height):
        for x in range(p.width):
            current_number = p.configuration[y][x]
            solved_y = (current_number-1)//p.width
            solved_x = current_number-1 - solved_y*p.width
            h += abs(solved_x-x) + abs(solved_y-y)

    return h/n

def rotation_neighbours(p: Puzzle):
    # Returns a list of puzzles with a configuration that can be reached from a given puzzle
    # by rotating a single 2x2 square block clockwise
    #   p:  NRP of class Puzzle

    neigh_list = []
    
    for y in range(p.height-1):
        for x in range(p.width-1):
            neigh_list.append(p.rotate(x,y))
            
    return neigh_list
            
def A_star(start: Puzzle):
    # Run an A* search to solve the given NRP using as a heuristic the average manhattan
    # distance and as cost the number of moves done
    #   start:  NRP of class Puzzle

    goal = Puzzle(start.width,start.height)

    q = [(0,start,[start])]
    heapq.heapify(q)

    g_scores = {start: 0}
    while len(q) != 0:
        current = heapq.heappop(q)
        if current[1] == goal:
            print("Solved in",g_scores[goal],"steps.")
            return current[2]

        for p in rotation_neighbours(current[1]):
            g = g_scores[current[1]]+1
            f = g + manhattan_heuristic(p)
            if p not in g_scores or g < g_scores[p]:
                heapq.heappush(q,(f,p,current[2]+[p]))
                g_scores[p] = g