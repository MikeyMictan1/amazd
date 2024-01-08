import random

def generate_maze(width, height):
    maze = [[1] * width for _ in range(height)]  # Create a grid filled with walls
    start_row = random.randrange(1, height, 2)
    start_col = random.randrange(1, width, 2)
    maze[start_row][start_col] = 0  # Set the starting cell as a path
    stack = [(start_row, start_col)]  # Stack to keep track of visited cells

    while stack:
        current_row, current_col = stack[-1]

        # Get unvisited neighbors
        unvisited_neighbors = []
        for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            new_row, new_col = current_row + dr, current_col + dc
            if 0 <= new_row < height and 0 <= new_col < width and maze[new_row][new_col] == 1:
                unvisited_neighbors.append((new_row, new_col))

        if unvisited_neighbors:
            new_row, new_col = random.choice(unvisited_neighbors)
            maze[new_row][new_col] = 0  # Carve a path
            maze[(current_row + new_row) // 2][(current_col + new_col) // 2] = 0  # Remove wall between cells
            stack.append((new_row, new_col))
        else:
            stack.pop()  # Backtrack if no unvisited neighbors

    return maze


def create_maze(maze):
    maze_lst = []
    rownum = -1
    for row in maze:
        maze_lst.append("".join(["XX" if cell == 1 else "  " for cell in row]))

    # creates walls as "Y" if they have space underneath them
    for row in maze_lst:
        rownum += 1
        colnum = -1

        for cell in row:  # checks ever cell
            colnum += 1
            if rownum == len(maze_lst) - 1:  # if it's the last row, make them all "Y" (NOTE TO SELF MAKE THE 21 (WHICH IS WIDTH) NOT HARDCODED)
                maze_lst[rownum] = maze_lst[rownum][:colnum] + "Y" + maze_lst[rownum][colnum + 1:]

            # if a cell is "X", and the cell beneath it is " " emtpy, make it into a "Y"
            elif cell == "X" and maze_lst[rownum + 1][colnum] == " ":
                maze_lst[rownum] = maze_lst[rownum][:colnum] + "Y" + maze_lst[rownum][colnum + 1:]

    # places the player in the top left corner every time, and a "Y" above them
    maze_lst[1] = maze_lst[1][:1] + "P" + maze_lst[1][2:]
    maze_lst[0] = maze_lst[0][:1] + "Y" + maze_lst[0][2:]
    return maze_lst

