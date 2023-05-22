import matplotlib.pyplot as plt
import numpy as np

from NRP import Puzzle
from search import search_runner

puzzle = Puzzle(3,3)
puzzle.shuffle(10)

result = search_runner(puzzle)
print(result)

rows = (len(result.puzzle_list)//4)+1
cols = 4

fig, ax = plt.subplots(nrows=rows, ncols=cols)

for row in range (rows):
    for col in range(cols):

        pos = (row*cols)+col
        if pos < len(result.puzzle_list):

            configs = np.array(result.puzzle_list[pos].configuration)


            im = ax[row, col].matshow(configs, cmap="tab10", interpolation='none')

            ax[row, col].set_xticks(np.arange(len(configs[0])))
            ax[row, col].set_yticks(np.arange(len(configs[0])))

            plt.setp(ax[row, col].get_xticklabels(), ha="right",
                     rotation_mode="anchor")

            # Loop over the values in the NRP and create text annotations.
            for i in range(len(configs[0])):
                for j in range(len(configs[0])):
                    text = ax[row, col].text(j, i, configs[i, j],ha="center", va="center", color="w")
            ax[row, col].set_title(str("Step " + str(pos+1)))

        else:
            ax[row, col].axis('off')

fig.tight_layout()
plt.show()