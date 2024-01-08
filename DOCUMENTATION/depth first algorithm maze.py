import pygame
import random

# Maze configuration
WIDTH = 800
HEIGHT = 600
ROWS = 40
COLS = 40
CELL_SIZE = WIDTH // COLS

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Maze grid
grid = [[0] * COLS for _ in range(ROWS)]

# Set start and end positions
start = (0, 0)
end = (ROWS - 1, COLS - 1)

# Directions
directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # Up, Right, Down, Left


def generate_maze():
    stack = [(start[0], start[1])]
    visited = set()
    while stack:
        x, y = stack[-1]
        grid[y][x] = 1  # Mark current cell as visited
        visited.add((x, y))

        unvisited_neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in visited:
                count = 0
                for ddx, ddy in directions:
                    nnx, nny = nx + ddx, ny + ddy
                    if 0 <= nnx < COLS and 0 <= nny < ROWS and grid[nny][nnx] == 1:
                        count += 1
                if count == 1:
                    unvisited_neighbors.append((nx, ny))

        if unvisited_neighbors:
            nx, ny = random.choice(unvisited_neighbors)
            stack.append((nx, ny))
        else:
            stack.pop()

    grid[start[1]][start[0]] = 2  # Mark start cell
    grid[end[1]][end[0]] = 3  # Mark end cell


def draw_maze():
    screen.fill(BLACK)

    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x] == 1:
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.update()


# Generate and draw the maze
generate_maze()
draw_maze()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)

# Quit the game
pygame.quit()