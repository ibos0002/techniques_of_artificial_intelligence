from NRP import Puzzle
from search import A_star

import random
import numpy as np


#Compute the effective branching factor of the heuristic for puzzles of size 3x3
b_star = 0

random.seed(10)
for i in range(100):
    print("Puzzle",i+1)
    p = Puzzle(3,3)
    p.shuffle(30)

    steps, N = A_star(p)
    d = len(steps)
    poly = [1 for _ in range(d+1)]
    poly[-1] -= N
    for root in np.roots(poly):
        if np.isreal(root):
            if root.real >= 0:
                b_star += root.real/100
                break

print("Branching factor: ", b_star)