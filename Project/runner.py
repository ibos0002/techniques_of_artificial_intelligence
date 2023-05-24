import matplotlib.pyplot as plt
import numpy as np

from NRP import Puzzle
from search import search_runner

def runner_GUI(width, height, columns=5):

    """ Runs the algorithm on a randomly generated puzzle of a given size
    and displays the steps nicely to the user
    Params:
    Width, height = integers, width and height of the random puzzle
    Columns = the number of steps (columns) to show on one line - the default is 5
    The number should be bigger for larger puzzles that require more steps,
    so it doesn't impact the visibility.
    """

    puzzle = Puzzle(width=width, height=height)
    puzzle.shuffle(width*height)

    result = search_runner(puzzle)
    print(result)

    rows = (len(result.puzzle_list) // columns) + 1
    cols = columns

    fig, ax = plt.subplots(nrows=rows, ncols=cols)

    for row in range(rows):
        for col in range(cols):

            pos = (row * cols) + col  # index of the configuration
            if pos < len(result.puzzle_list):

                # create a np array of each configuration
                configs = np.array(result.puzzle_list[pos].configuration)

                # create the heatmap of the configuration
                im = ax[row, col].matshow(configs, cmap="Set3", interpolation="None")

                ax[row, col].set_xticks(np.arange(width))
                ax[row, col].set_yticks(np.arange(height))

                plt.setp(ax[row, col].get_xticklabels(), ha="right",rotation_mode="anchor")

                # Loop over the values in the NRP and create text annotations
                for i in range(height):
                    for j in range(width):
                        text = ax[row, col].text(j, i, configs[i, j], ha="center", va="center", color="black")
                ax[row, col].set_title(str("Step " + str(pos + 1)))

            else:
                ax[row, col].axis('off')

    fig.tight_layout()
    plt.show()

runner_GUI(width= 3, height= 3)
