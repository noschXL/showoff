import sys
import pygame
import os
from math import floor
from Spritesheet import spritesheet
from settings import *

path = os.path.abspath(os.path.dirname(__file__))

lastInput = False

selected = None  # always None or [x,y] of the board location

clock = pygame.time.Clock()

def parseFen(notation: str):
    rowsizes = []
    needed_fields = 0

    for char in notation:
        try:
            needed_fields += int(char)
            continue

        except ValueError:
            if char in ["r","n","b","q","k","p","R","N","B","Q","K","P"]:
                needed_fields += 1
            elif char == "/":
                rowsizes.append(needed_fields)
                needed_fields = 0
            else:
                raise ValueError(f"unknown FEN character: {char}")

    rowsizes.append(needed_fields)

    corrupted = False
    for i in range(0,8):
        if rowsizes[i] != 8:
            corrupted = True

    if len(rowsizes) != 8 or corrupted:
        raise ValueError(f"corrupted FEN string wich needs {len(rowsizes)} rows and the following setup of rows: {rowsizes} to be played")

    # beginn actual parsing

    board = [[EMPTY] * 8 for _ in range(8)]
    colum = 0
    row = 0
    for char in notation:
        if char.lower() == "p":
            board[row][colum] = PAWN + (BLACK if char.lower() == char else WHITE)
            colum += 1
        elif char.lower() == "b":
            board[row][colum] = BISHOP + (BLACK if char.lower() == char else WHITE)
            colum += 1
        elif char.lower() == "n":
            board[row][colum] = KNIGHT + (BLACK if char.lower() == char else WHITE)
            colum += 1
        elif char.lower() == "r":
            board[row][colum] = ROOK + (BLACK if char.lower() == char else WHITE)
            colum += 1
        elif char.lower() == "q":
            board[row][colum] = QUEEN + (BLACK if char.lower() == char else WHITE)
            colum += 1
        elif char.lower() == "k":
            board[row][colum] = KING + (BLACK if char.lower() == char else WHITE)
            colum += 1
        elif char == "/":
            row += 1
            colum = 0
        else:
            colum += int(char)
    
    return board

def parsemouse(board: list[list[int]], player: bool):
    global lastInput
    global selected

    clicked = False
    pressed = pygame.mouse.get_pressed()[0] # check only the first mouse button (left mouse button)

    if not lastInput and pressed:  #only on first press
        clicked = True

    lastInput = pressed

    if selected is not None:
        pygame.draw.rect(screen, "#F9E076", (selected[0] * 70, selected[1] * 70, 70, 70))

    if not clicked:
        return player, board
    
    x, y = pygame.mouse.get_pos()
    x, y = floor(x / 70), floor(y / 70)

    if  (selected is None and board[y][x] & WHITE != player) or (board[y][x] != EMPTY and board[y][x] & WHITE != player and not [x,y] == selected):  #TODO: make it cleaner

        selected = [x,y]
        print((get_moves(board, [0,1])))

    elif selected is not None and [x,y] != selected and (board[y][x] == EMPTY or board[y][x] // 8 == player):
        board[y][x] = board[selected[1]][selected[0]]
        board[selected[1]][selected[0]] = EMPTY
        selected = None
        player = not player
    else:
        selected = None

    return player, board

def drawSquares(screen: pygame.Surface):
    for x in range(8):
        for y in range(8):
            color = WHITECOLOR if (x+y) % 2 == 0 else BLACKCOLOR
            pygame.draw.rect(screen, color, (x * 70, y * 70, 70, 70))

def drawPieces(screen: pygame.Surface, board: list[list[int]], images: list[pygame.Surface]):
    for y in range(8): #down
        for x in range(8): #right
            if board[y][x] == EMPTY:
                pass
            else:
                screen.blit(images[board[y][x] - 1 - WHITE -  (2 if board[y][x] - WHITE >= 8 else 0)  ], (x * 70,y * 70,70,70))
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