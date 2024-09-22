import pygame

pygame.init()

ROOT, TOP, RIGHT, DOWN, LEFT = -1, 1, 2, 3, 4

def drawWalls(screen:pygame.Surface, maze:list[list[int]], size: list[int,int] = [600,600]):

    size = [size[0] - 20, size[1] - 20]

    mazeHeight = len(maze)
    mazeWidth = len(maze[0])

    squareMaxWidth = size[0] / mazeWidth
    squareMaxHeight = size[1] / mazeHeight

    squareLenght = min(squareMaxHeight, squareMaxWidth)

    print(f"{__file__}: square Lenght set to {squareLenght}")

    walls:list[bool] = [False] * 4

    for y, row in enumerate(maze):
        for x, dir in enumerate(row):
            if dir != ROOT:
                print(walls)
                walls[dir - 1] = True

            if y - 1 >= 0 and maze[y - 1][x] != DOWN:
                walls[0] = True
            if y + 1 < mazeHeight and maze[y + 1][x] != TOP:
                walls[2] = True

            if x - 1 >= 0 and maze[y][x - 1] != RIGHT:
                walls[1] = True
            if x + 1 < mazeWidth and maze[y][x + 1] != LEFT:
                walls[3] = True

            print(f"{__file__}: walls: {walls}, x,y: {x,y}")

if __name__ == "__main__":
    drawWalls(1, [[0,1,2,3],1,2,3], )