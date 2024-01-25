import random

#maze_width = 21
#maze_height = 21


class df_maze_generation:
    def __init__(self, maze_width, maze_height):
        self.df_maze = []
        self.maze_width = maze_width
        self.maze_height = maze_height

    def main_code(self):
        # generating the maze
        for row in range(self.maze_height):
            maze_row = []  # makes a row list for the inputted height

            for cell in range(self.maze_width):
                maze_row.append("X")  # fills the row with "x", by the width number
            self.df_maze.append(maze_row)

        visited_cells_stack = [
            (1, 1)]  # where the stack starts (and where we start the maze), the stack holds ALL visited cells

        while visited_cells_stack != []:
            current_row, current_col = visited_cells_stack[-1]
            unvisited_neighbors = []

            # finding all unvisited neighbours
            up = (current_row + 2, current_col)
            down = (current_row - 2, current_col)
            left = (current_row, current_col + 2)
            right = (current_row, current_col - 2)

            up_neighbours = self.find_neighbours(up)
            if up_neighbours != None:
                unvisited_neighbors.append(up_neighbours)

            down_neighbours = self.find_neighbours(down)
            if down_neighbours != None:
                unvisited_neighbors.append(down_neighbours)

            left_neighbours = self.find_neighbours(left)
            if left_neighbours != None:
                unvisited_neighbors.append(left_neighbours)

            right_neighbours = self.find_neighbours(right)
            if right_neighbours != None:
                unvisited_neighbors.append(right_neighbours)

            # if we have unvisited neighbours, pick one at random
            if unvisited_neighbors != []:
                new_row, new_col = random.choice(unvisited_neighbors)
                self.df_maze[new_row][new_col] = "V"  # Creates the path
                self.df_maze[(current_row + new_row) // 2][(current_col + new_col) // 2] = "V"  # Remove wall
                visited_cells_stack.append((new_row, new_col))

            else:
                visited_cells_stack.pop()

        return self.df_maze

    def find_neighbours(self, direction):
        if (direction[0] < self.maze_height and direction[0] > 0) and (
                direction[1] < self.maze_width and direction[1] > 0) and \
                self.df_maze[direction[0]][direction[1]] == "X":
            return (direction[0], direction[1])
        else:
            return None

    def create_maze(self):
        maze_lst = []
        rownum = -1
        placed_portal = False

        for row in self.df_maze:
            maze_lst.append("".join(["XX" if cell == "X" else "  " for cell in row]))

        # creates walls as "Y" if they have space underneath them
        for row in maze_lst:
            rownum += 1
            colnum = -1

            for cell in row:  # checks every cell !
                powerup_chance = random.randint(0, 50)  # a one in 50 chance POWERUP CHANCE ----------------
                enemy_chance = random.randint(0,20)
                coin_chance = random.randint(0, 20)
                exit_chance = random.randint(0, 10)





                colnum += 1


                if rownum == len(
                        maze_lst) - 1:  # if it's the last row, make them all "Y"
                    maze_lst[rownum] = maze_lst[rownum][:colnum] + "Y" + maze_lst[rownum][colnum + 1:]

                # if a cell is "X", and the cell beneath it is " " emtpy, make it into a "Y"
                elif cell == "X" and maze_lst[rownum + 1][colnum] == " ":
                    maze_lst[rownum] = maze_lst[rownum][:colnum] + "Y" + maze_lst[rownum][colnum + 1:]

                # adding powerups to the map
                if cell == " " and powerup_chance == 0:
                    maze_lst[rownum] = maze_lst[rownum][:colnum] + "U" + maze_lst[rownum][colnum + 1:]

                # adding coins to the map
                if cell == " " and coin_chance == 0:
                    maze_lst[rownum] = maze_lst[rownum][:colnum] + "C" + maze_lst[rownum][colnum + 1:]

                # adding enemies to the map
                elif cell == " " and enemy_chance == 0:
                    maze_lst[rownum] = maze_lst[rownum][:colnum] + "E" + maze_lst[rownum][colnum + 1:]


                #  Creating the exit
                if (colnum == len(maze_lst[0])-3) and (placed_portal == False) and (exit_chance == 0):
                    maze_lst[rownum] = maze_lst[rownum][:colnum] + "O" + maze_lst[rownum][colnum + 1:]
                    placed_portal = True

                if (colnum == len(maze_lst[0])-3) and (rownum == len(maze_lst)-1) and (placed_portal == False):
                    #print("REACHED END OF THE MAZE, MAKING DEFAULT EXIT")
                    maze_lst[rownum] = maze_lst[rownum][:colnum] + "O" + maze_lst[rownum][colnum + 1:]
                    placed_portal = True



        # places the player in the top left corner every time, and a "Y" above them
        maze_lst[1] = maze_lst[1][:1] + "P" + maze_lst[1][2:]
        maze_lst[0] = maze_lst[0][:1] + "Y" + maze_lst[0][2:]
        return maze_lst


# ------------------------------


#depth_first_maze = df_maze_generation(maze_width, maze_height)
#depth_first_maze.main_code()
#maze = depth_first_maze.create_maze()
