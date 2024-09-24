import sys
import pygame
import os
from math import floor
from Spritesheet import spritesheet
from settings import *
from Renderer import *
from MoveGenerator import GetMoves
from helper import parseFen, clear_bit

path = os.path.abspath(os.path.dirname(__file__))

lastInput = False

selected = None  # always None or [x,y] of the board location

clock = pygame.time.Clock()

def parsemouse(board: list[list[int]], player: bool):
    global lastInput
    global selected

    clicked = False
    pressed = pygame.mouse.get_pressed()[0] # check only the first mouse button (left mouse button)

    if not lastInput and pressed:  #only on first press
        clicked = True

    lastInput = pressed

    if selected is not None:
        pygame.draw.rect(screen, "#F9E076", (selected[1] * 70 * sizefactor, selected[0] * 70 * sizefactor, 70 * sizefactor, 70 * sizefactor))

    if not clicked:
        return player, board
    
    x, y = pygame.mouse.get_pos()
    x, y = floor(x / (70 * sizefactor)), floor(y / (70 * sizefactor))

    color = not (board[y][x] >> 3) - 1

    if color == player and board[y][x]:
        selected = [y,x]

    elif selected is not None and [y, x] in GetMoves(board, selected, allowed):

        type = board[selected[0]][selected[1]]
        color = type >> 3
        type = clear_bit(type, 3)
        type = clear_bit(type, 4)

        if type == KING:
            if color == 1:
                if selected[1] - x == 2:
                    board[y][x + 1] = board[y][0]
                    board[y][0] = EMPTY
                elif selected[1] - x == -2:
                    board[y][x - 1] = board[y][7]
                    board[y][7] = EMPTY
            elif color == 2:
                if selected[1] - x == 2:
                    board[y][x + 1] = board[y][0]
                    board[y][0] = EMPTY
                elif selected[1] - x == -2:
                    board[y][x - 1] = board[y][7]
                    board[y][7] = EMPTY

        board[y][x] = board[selected[0]][selected[1]]

        board[selected[0]][selected[1]] = EMPTY

        selected = None
        player = not player

    else:
        selected = None

    return player, board

screen = pygame.display.set_mode((70 * 8 * sizefactor, 70 * 8 * sizefactor))

whiteSpriteSheet = spritesheet(os.path.join(path, "img", "pieces_white.png"))
blackSpriteSheet = spritesheet(os.path.join(path, "img", "pieces_black.png"))

imgrects = [(x * 32,0,32,32) for x in range(6)]
images = [] + whiteSpriteSheet.images_at(imgrects, (255,0,0))
images += blackSpriteSheet.images_at(imgrects, (255,0,0))

newimgs = []
if sizefactor != 1:
    for img in images:
        newimgs.append(pygame.transform.scale_by(img, sizefactor))

    images = newimgs


board, allowed = parseFen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

player = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    drawSquares(screen)
    player, board = parsemouse(board, player)
    drawPieces(screen, board, images)


    pygame.display.flip()
    clock.tick(60)