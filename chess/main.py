import sys
import pygame
import os
from math import floor
from Spritesheet import spritesheet
from settings import *
from Renderer import *
from MoveGenerator import Checkmated, GetLegalMoves
from helper import parseFen, MoveTo

path = os.path.abspath(os.path.dirname(__file__))

lastInput = False

selected = None
moves = None

clock = pygame.time.Clock()

def parsemouse(board: list[list[int]], player: bool, allowed: str):
    global lastInput
    global selected
    global moves

    clicked = False
    pressed = pygame.mouse.get_pressed()[0] # check only the first mouse button (left mouse button)

    if not lastInput and pressed:  #only on first press
        clicked = True

    lastInput = pressed

    drawSelected(screen, selected)

    drawMoveable(screen, moves)

    if not clicked:
        return player, board, allowed
    
    x, y = pygame.mouse.get_pos()
    x, y = floor(x / (70 * sizefactor)), floor(y / (70 * sizefactor))

    color = not (board[y][x] >> 3) - 1

    if color == player and board[y][x]:
        selected = [y,x]
        moves = GetLegalMoves(board, selected, allowed)

    elif selected is not None and [y, x] in moves:

        board, allowed = MoveTo(board, [y, x], selected, allowed)

        selected = None
        moves = None
        player = not player

    else:
        selected = None
        moves = None

    return player, board, allowed

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

#org: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

board, allowed, player = parseFen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    drawSquares(screen)
    player, board, allowed = parsemouse(board, player, allowed)
    drawPieces(screen, board, images)


    pygame.display.flip()

    if Checkmated(board, player, allowed):
        print(f"oh no, {"white" if player else "black"} lost the game, gg.")
        drawBoard(screen, board, images)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    clock.tick(60)