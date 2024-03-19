import random


class DepthFirstMaze:
    """
    Description:
        Class that creates the recursive depth-first maze.

    Attributes:
        df_maze (list):
        __maze_width (int):
        __maze_height (int):

        visited_cells_stack (list):
        placed_portal (bool):
        maze_lst (list):
        __row_num (int):
    """
    def __init__(self, maze_width: int, maze_height: int):
        """
        Description:
            Initialisation function for the game change class.
        """
        self.df_maze = []
        self.__maze_width = maze_width
        self.__maze_height = maze_height
        # where the stack starts (and where we start the maze), the stack holds visited cells before backtracking
        self.visited_cells_stack = [(1, 1)]
        self.placed_portal = False
        self.maze_lst = []
        self.__row_num = -1

    def __generate_blank_maze(self):
        """
        Description:
            creates a blank maze of only walls based on maze dimensions
        """
        for row in range(self.__maze_height):
            maze_row = []  # makes a row list for the inputted height

            for cell in range(self.__maze_width):
                maze_row.append("X")  # fills the row with "x", by the width number
            self.df_maze.append(maze_row)  # we now have a list made of just rows of walls (X)

    def __find_neighbours(self, direction: tuple):
        """
        Description:
            used in depth first maze generation, finds all neighbour cells of the current cell, and returns neighbour
            cells if then haven't been visited.

        Parameters:
            direction (tuple): The direction that the neighbour cell is, relative to the current cell.

        Returns:
            direction: returns the direction of the neighbour cell if it is in bounds, and unvisited
            None: returns none if the neighbour cell is either out of bounds, or has been visited
        """
        direction_row = direction[0]
        direction_column = direction[1]
        # if the neighbour cell we want to travel to is in bounds, and is a wall (unvisited cell), then return that cell
        if ((self.__maze_height > direction_row > 0) and (self.__maze_width > direction_column > 0) and \
                (self.df_maze[direction[0]][direction[1]] == "X")):

            return direction

        else:  # else, we can't travel to that cell so return None
            return None

    def __create_recursive_maze(self, recursive_stack: list):
        """
        Description:
            Creates the recursive depth first generated maze.

        Parameters:
            recursive_stack (list): The recursive stack of visited cells that gets passed through each recursive case

        Returns:
            df_maze (list): The final depth-first maze, represented as a list. returns in the base case.
            __create_recursive_maze(recursive_stack): The method recursively goes through itself until the base case
            is reached.
        """
        # BASE CASE
        if not recursive_stack:
            return self.df_maze

        # RECURSIVE CASE
        else:
            unvisited_neighbor_cells = []
            # our current row and column becomes the top of the stack
            current_row = recursive_stack[-1][0]
            current_column = recursive_stack[-1][1]

            # neighbours
            up_neighbour = (current_row + 2, current_column)
            down_neighbour = (current_row - 2, current_column)
            left_neighbour = (current_row, current_column + 2)
            right_neighbour = (current_row, current_column - 2)
            possible_directions = [up_neighbour, down_neighbour, left_neighbour, right_neighbour]

            # for every neighbour of a cell in a possible direction
            for direction_cell in possible_directions:
                cell_neighbour = self.__find_neighbours(direction_cell)
                if cell_neighbour:  # if it has unvisited neighbours, then append to unvisited neighbours
                    unvisited_neighbor_cells.append(cell_neighbour)

            # if we have unvisited neighbours, pick one at random and carve path to it
            if unvisited_neighbor_cells:
                new_cell = random.choice(unvisited_neighbor_cells)
                new_row = new_cell[0]
                new_column = new_cell[1]

                # removes wall at current cell
                self.df_maze[new_row][new_column] = " "
                # Removes wall between previous cell and current one
                self.df_maze[(current_row + new_row) // 2][(current_column + new_column) // 2] = " "
                recursive_stack.append((new_row, new_column))  # adds cell to stack

            else:  # if no unvisited neighbours, then backtrack by one
                recursive_stack.pop()

            return self.__create_recursive_maze(recursive_stack)

    def __add_elements_to_maze(self):
        """
        Description:
            Adds powerups, player, portal, to the maze and increases the width of the depth-first generated maze.

        Returns:
            maze_lst (list): The final maze list, complete with powerups, player, portal
        """
        for row in self.df_maze:
            extended_row = []

            for cell in row:
                if cell == "X":
                    extended_row.append("XX")
                else:
                    extended_row.append("  ")

            self.maze_lst.append("".join(extended_row))

        for row in self.maze_lst:
            self.__row_num += 1
            self.col_num = -1

            for self.cell in row:  # checks every cell !
                powerup_chance = random.randint(0, 50)  # a one in 50 chance
                enemy_chance = random.randint(0, 20)
                coin_chance = random.randint(0, 20)
                exit_chance = random.randint(0, 10)
                health_pot_chance = random.randint(0, 100)

                self.col_num += 1

                # --- ADDING "Y" WALLS FOR MAZE WALLS TO HAVE DEPTH ---
                if self.__row_num == len(self.maze_lst) - 1:  # if it's the last row, make them all "Y"
                    self.__place_item_in_maze("Y")

                elif self.cell == "X" and self.maze_lst[self.__row_num + 1][self.col_num] == " ":
                    self.__place_item_in_maze("Y")

                # --- ADDING POWERUPS, ENEMIES TO MAZE ---
                self.__random_spawn_chance(powerup_chance, "U")
                self.__random_spawn_chance(coin_chance, "C")
                self.__random_spawn_chance(health_pot_chance, "H")
                self.__random_spawn_chance(enemy_chance, "E")

                #  --- CREATING THE EXIT ---
                if (self.col_num == len(self.maze_lst[0]) - 3) and (self.placed_portal == False) and (
                        exit_chance == 0):
                    self.__place_item_in_maze("O")
                    self.placed_portal = True

                #  if no exit already made, then make this default exit
                elif (self.col_num == len(self.maze_lst[0]) - 3) and (self.__row_num == len(self.maze_lst) - 1) and (
                        self.placed_portal == False):
                    self.__place_item_in_maze("O")
                    self.placed_portal = True

        # places the player in the top left corner every time, and a "Y" above them
        self.maze_lst[1] = self.maze_lst[1][:1] + "P" + self.maze_lst[1][2:]
        self.maze_lst[0] = self.maze_lst[0][:1] + "Y" + self.maze_lst[0][2:]
        return self.maze_lst

    # used in add_elements_to_maze for collidables to be added to the maze
    def __random_spawn_chance(self, spawn_probability: int, spawn_letter: str):
        """
        Description:
            Will put a certain element (such as a powerup) on a cell in the maze, if the random probability of the
            element lands on 0.

        Parameters:
            spawn_probability (int): The randomly generated number that dictates how likely an element is to be put in
            the maze.
            spawn_letter (str): The letter of the element to be potentially put in the maze
        """
        if self.cell == " " and spawn_probability == 0:
            self.__place_item_in_maze(spawn_letter)

    def __place_item_in_maze(self, spawn_letter: str):
        """
        Description:
            Places the player, portal, and "Y" walls to the maze.

        Parameters:
            spawn_letter (str):  he letter of the element to be put in the maze
        """
        self.maze_lst[self.__row_num] = self.maze_lst[self.__row_num][:self.col_num] + spawn_letter + self.maze_lst[
                                                                                                          self.__row_num][
                                                                                                      self.col_num + 1:]

    def create_maze(self):
        """
        Description:
            Creates the entire maze, as it runs most of the other methods in the class.

        Returns:
            __add_elements_to_maze: This will return the final maze as a list.
        """
        self.__generate_blank_maze()
        self.__create_recursive_maze(self.visited_cells_stack)
        return self.__add_elements_to_maze()
