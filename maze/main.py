import Generator
import Renderer
import random
import pygame

ROOT, TOP, RIGHT, DOWN, LEFT = -1, 1, 2, 3, 4

directions = [TOP, RIGHT, DOWN, LEFT]

maze, root = Generator.newMaze(5,5)
step = 1
while True:
    direction = random.choice(directions)
    maze, root = Generator.moveRoot(maze, root, direction)

    for row in maze:
        print(row)
    if step == 1:
        Renderer.drawWalls(1, maze)
    else:
        break

    print(f"done step: {step}")
    step += 1