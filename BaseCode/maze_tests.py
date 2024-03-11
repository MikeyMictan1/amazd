from maze import DepthFirstMaze

# --- Initial Tests Setup ---
test_maze_width = 7
test_maze_height = 7

test_maze = DepthFirstMaze(test_maze_width, test_maze_height)
test_maze.create_maze()
# --- Initial Tests Setup ---


def testing_maze_size():  # tests the size of the maze is correct
    assert len(test_maze.df_maze) == test_maze_height, "Number of rows not equal to height for initial df maze"
    assert len(test_maze.maze_lst) == test_maze_height, "Number of rows not equal to height"
    assert all(len(row) == test_maze_width * 2 for row in test_maze.maze_lst), "Every row is not 2x width"


def testing_player_and_exit():  # tests there is an exit and player in the maze, and only one of them
    player_found = False
    exit_found = False
    player_count = 0
    exit_count = 0

    for row in test_maze.maze_lst:
        for cell in row:
            if cell == "P":
                player_found = True
                player_count += 1

            if cell == "O":
                exit_found = True
                exit_count += 1

    assert player_found, "Player not found in the maze"
    assert player_count == 1, "More than one, or no players found"
    assert exit_found, "Exit not found in the maze"
    assert exit_count == 1, "More than one, or no exits found"
    assert test_maze.placed_portal, "Portal not placed"


def testing_recursive_stack():  # tests that the recursive stack should be empty
    assert not test_maze.visited_cells_stack, "Recursive stack is not empty"


def testing_maze_walls():  # checks if there are walls of both "X" and "Y" in the correct places
    row_num = -1
    for row in test_maze.maze_lst:
        row_num += 1
        col_num = -1
        for cell in row:
            col_num += 1
            if col_num == test_maze_width*2 and cell != "Y":
                assert cell == "X", "No wall present to the right side of the maze"

            if col_num == 0 and cell != "Y":
                assert cell == "X", "No wall present to the left side of the maze"

            if cell not in " YUCHEPO":
                assert cell == "X", "Wall cell not present where it should be"

            if row_num == len(test_maze.maze_lst) - 1 and cell != "O":
                assert cell == "Y", "No wall present at the bottom of the maze"

            if cell not in " XUCHEPO" and test_maze.maze_lst[row_num + 1][col_num] == " ":
                assert cell == "Y", "Walls that are below empty space are the wrong cell"































