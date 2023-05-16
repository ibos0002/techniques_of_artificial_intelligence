from __future__ import annotations
from random import randrange
from typing import Optional

def solved_puzzle(width: int, height: int):
    # Returns a solved number rotation puzzle of given height and width
    #   width:      width of the puzzle
    #   height:     height of the puzzle

    return tuple([tuple([i+j*width+1 for i in range(width)]) for j in range(height)])

def list_to_tuple(configuration: list[list[int]]):
    # Convert a configuration given as a list of lists into a tuple of tuples
    #   configuration:      configuration to be converted

    tuple_configuration = []
    for row in configuration:
        tuple_configuration.append(tuple(row))
    return tuple(tuple_configuration)

class Puzzle():
    def __init__(self, width: Optional[int] = None, height: Optional[int] = None,
                 configuration: Optional[tuple[tuple[int]]] = None):
        # Initializes the puzzle as a solved puzzle of given width and height
        #   width:          width of the puzzle. Optional parameter if configuration is given and is
        #                   then equal to the width of that configuration
        #   height:         height of the puzzle. Optional parameter if configuration is given and is
        #                   then equal to the height of that configuration
        #   configuration:  tuple of tuples representing the configuration of the puzzle
        #                   Optional parameter if height and width are not given.
        #                   If configuration is not given, self.configuration is the solved
        #                   configuration with the corresponding height and width

        if configuration is None:
            if width is None or height is None:
                raise ValueError("Either configuration or width and height must be given!")
            self.configuration = solved_puzzle(width,height)
            self.width = width
            self.height = height
        else:
            self.configuration = list_to_tuple(configuration)
            self.height = len(configuration)
            self.width = len(configuration[0])

    def __str__(self):
        # Returns an easily readable string representing the puzzle's current configuration

        output_string = ""
        max_value = self.width*self.height
        max_digits = len(str(max_value))
        for i in range(self.height):
            for j in range(self.width):
                current_number = str(self.configuration[i][j])
                current_digits = len(current_number)
                output_string +=  " "*(max_digits-current_digits) + current_number

                if j != self.width-1:
                    output_string += " "

            if i != self.height-1:
                output_string += "\n"

        return output_string

    def __hash__(self):
        return hash(self.configuration)

    def __eq__(self, other: Puzzle):
        return self.configuration == other.configuration

    def __lt__(self, other: Puzzle):
        if any([None in row for row in self.configuration]):
            return True
        return self.configuration.__lt__(other.configuration)

    def rotate(self, x: int, y: int, configuration: Optional[list[list[int]]] = None):
        # Either creates a new puzzle, by rotating the 2x2 square block in the puzzle and
        # returns the corresponding new NRP of class Puzzle or if configuration is given,
        # rotates the corresponding 2x2 square block in configuration and returns the new
        # configuration as a list of lists
        #
        #   x:              x-coordinate of the 2x2 square in the puzzle
        #   y:              y-coordinate of the 2x2 square in the puzzle
        #   configuration:  list of lists representing the desired configuration
        #                   Optional parameter. If not given, self.configuration is taken instead

        if configuration is None:
            config = self.configuration
            puzzle_return = True
        else:
            config = configuration
            puzzle_return = False

        rotation_map = {(y,x):(y+1,x),
                        (y,x+1):(y,x),
                        (y+1,x+1):(y,x+1),
                        (y+1,x):(y+1,x+1)}

        new_configuration = []
        for j in range(self.height):
            config_row = []
            for i in range(self.width):
                if (j,i) in rotation_map:
                    config_row.append(config[rotation_map[(j,i)][0]][rotation_map[(j,i)][1]])
                else:
                    config_row.append(config[j][i])

            if puzzle_return:
                new_configuration.append(tuple(config_row))
            else:
                new_configuration.append(config_row)

        if puzzle_return:
            return Puzzle(self.width,self.height,tuple(new_configuration))
        else:
            return new_configuration

    def shuffle(self,number_rotations):
        # Randomly shuffles the puzzle by randomly rotating 2x2 squares and assigns the new
        # shuffled configuration to the NRP instance self
        #   number_rotations:   number of rotations to be done

        config = self.configuration

        for _ in range(number_rotations):
            x = randrange(0,self.width-1)
            y = randrange(0,self.height-1)
            config = self.rotate(x,y,configuration=config)

        final_config = []
        for row in config:
            final_config.append(tuple(row))

        self.configuration = tuple(final_config)

class Puzzle_solution:
    def __init__(self,p: Puzzle, rotation_list: list[tuple[int]]):
        # Intializes the puzzle solution using the initial puzzle and the rotations required to solve it
        # by generating the intermediate puzzles and computing the number of steps
        #   p:              instance of Puzzle to be solved
        #   rotation_list:  list of rotations required to solved the puzzle

        self.p = p

        puzzle_list = [p]
        for rot in rotation_list:
            p = p.rotate(rot[0],rot[1])
            puzzle_list.append(p)
        self.puzzle_list = puzzle_list

        self.rotation_list = rotation_list
        self.num_steps = len(rotation_list)

    def __str__(self):
        # Returns an easily readable string representing the steps required to solve the
        # initial puzzle and the intermediate puzzles
        output_str = ""
        max_value = self.p.width*self.p.height
        max_digits = len(str(max_value))

        for step,tup in enumerate(zip(self.rotation_list,self.puzzle_list[:-1])):
            rot, p = tup
            output_str += "Step "+str(step+1)+"\n"
            top_y = rot[1]
            bottom_y = rot[1]+1
            left_x = rot[0]
            right_x = rot[0]+1
            for y in range(p.height):
                row_str = "\t"
                for x in range(p.width):
                    current_number = str(p.configuration[y][x])
                    current_digits = len(current_number)
                    if x == left_x and y in [top_y,bottom_y]:
                        row_str += "|"
                    else:
                        if not (x == right_x+1 and y in [top_y,bottom_y]):
                            row_str += " "

                    if x == right_x+1 and y in [top_y,bottom_y]:
                        row_str += " "*(max_digits-current_digits-1)+"|"
                    else:
                        row_str += " "*(max_digits-current_digits)
                    row_str += current_number

                    if x == p.width-1:
                        if x == right_x and y in [top_y,bottom_y]:
                            row_str += "|"+(max_digits-current_digits-1)*" "

                row_str += "\n"

                output_str += row_str

        output_str += "Final solution\n"
        p = self.puzzle_list[-1]

        for y in range(p.height):
            row_str = "\t"
            for x in range(p.width):
                current_number = str(p.configuration[y][x])
                current_digits = len(current_number)

                row_str += " "*(max_digits-current_digits+1)
                row_str += current_number

            row_str += "\n"
            output_str += row_str

        output_str += "\nSolved in " +str(self.num_steps)+ " steps."

        return output_str
