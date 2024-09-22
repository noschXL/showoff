import random

# Direction constants
ROOT, TOP, RIGHT, DOWN, LEFT = -1, 1, 2, 3, 4

def newMaze(width: int, height: int) -> tuple[list[list[int]], list[int]]:
    """Returns a default maze and root position"""
    maze = [[RIGHT for x in range(width)] for y in range(height)]
    for y in range(height):
        maze[y][-1] = DOWN
    maze[-1][-1] = ROOT
    return maze, [height - 1, width - 1]

def moveRoot(maze: list[list[int]], root: list[int] | None = None, direction: int = TOP) -> tuple[list[list[int]], list[int]]:
    """Moves the root in the specified direction. Finds root if not provided."""
    
    # If root is None, find the root in the maze
    if root is None:
        for y, row in enumerate(maze):
            if ROOT in row:
                root = [y, row.index(ROOT)]
                break

    y, x = root
    maze[y][x] = direction  # Set current root position to the direction of movement

    if direction == TOP and y > 0:
        y -= 1
    elif direction == RIGHT and x < len(maze[0]) - 1:
        x += 1
    elif direction == DOWN and y < len(maze) - 1:
        y += 1
    elif direction == LEFT and x > 0:
        x -= 1

    maze[y][x] = ROOT  # Place the root at the new position
    root = [y, x]      # Update root coordinates

    return maze, root

def generateMaze(width: int, height: int, steps: int) -> list[list[int]]:
    """Generates a maze by moving the root randomly multiple times"""
    maze, root = newMaze(width, height)

    # Define all possible directions
    directions = [TOP, RIGHT, DOWN, LEFT]

    for _ in range(steps):
        # Choose a random valid direction
        direction = random.choice(directions)
        maze, root = moveRoot(maze, root, direction)

    return maze

if __name__ == "__main__":
    width, height = 5, 4
    steps = (width * height) ** 2  # Number of steps to move the root

    # Generate the maze
    maze = generateMaze(width, height, steps)

    # Print the final maze
    print("Final generated maze:")
    for row in maze:
        print(row)
