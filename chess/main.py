import sys
import pygame
import os
from math import floor
from Spritesheet import spritesheet
from settings import *
from Renderer import *
from MoveGenerator import GetMoves
from helper import parseFen

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
        pygame.draw.rect(screen, "#F9E076", (selected[1] * 70, selected[0] * 70, 70, 70))

    if not clicked:
        return player, board
    
    x, y = pygame.mouse.get_pos()
    x, y = floor(x / 70), floor(y / 70)

    color = not (board[y][x] >> 3) - 1

    if selected is None and color == player and board[y][x]:
        selected = [y,x]
        moves = GetMoves(board, selected)
        print(moves, selected)

    elif selected is not None and [y, x] in GetMoves(board, selected):
        board[y][x] = board[selected[0]][selected[1]]
        board[selected[0]][selected[1]] = EMPTY
        selected = None
        player = not player
    else:
        selected = None

    return player, board

screen = pygame.display.set_mode((70 * 8, 70 * 8))

whiteSpriteSheet = spritesheet(os.path.join(path, "img", "pieces_white.png"))
blackSpriteSheet = spritesheet(os.path.join(path, "img", "pieces_black.png"))

imgrects = [(x * 32,0,32,32) for x in range(6)]
images = [] + whiteSpriteSheet.images_at(imgrects, (255,0,0))
images += blackSpriteSheet.images_at(imgrects, (255,0,0))

board = parseFen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

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