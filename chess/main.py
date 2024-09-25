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

def parsemouse(board: list[list[int]], player: bool, allowed: str):
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
        return player, board, allowed
    
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

        fenComp = allowed.split()

        toRem = None

        if type == KING:
            if color == 1:
                if selected[1] - x == 2:    #queenside
                    board[y][x + 1] = board[y][0]
                    board[y][0] = EMPTY
                elif selected[1] - x == -2: #kingside
                    board[y][x - 1] = board[y][7]
                    board[y][7] = EMPTY
                toReml = "KQ"
            elif color == 2:
                if selected[1] - x == 2:    #queenside
                    board[y][x + 1] = board[y][0]
                    board[y][0] = EMPTY
                elif selected[1] - x == -2: #kingside
                    board[y][x - 1] = board[y][7]
                    board[y][7] = EMPTY
                toReml = "kq"

            if toReml is not None:
                for toRem in toReml:
                    fenComp[0] = fenComp[0].replace(toRem, "")

                if len(fenComp[0]) == EMPTY:
                        fenComp[0] = "-"

        print(fenComp)

        if type == PAWN:
            if fenComp[1] != "-":
                if [int(fenComp[1][1]), BOTTOMLETTERS.index(fenComp[1][0])] == [y,x]:
                    if color == 1:     #white
                        board[y + 1][x] = EMPTY
                    elif color == 2:   #black
                        board[y + 1][x] = EMPTY

            fenComp[1] = "-"

            if color == 1 and abs(selected[0] - y) == 2: #white
                fenComp[1] = BOTTOMLETTERS[x] + str(y + 1)
            elif color == 2 and abs(selected[0] - y) == 2: #black
                fenComp[1] = BOTTOMLETTERS[x] + str(y - 1)

            print(fenComp)


        print(fenComp)

        allowed = fenComp[0] + " " + fenComp[1] + " " + fenComp[2] + " " + fenComp[3]


# i took pasant if pawn on takepassante

        allowed = fenComp[0] + " " + fenComp[1] + " " + fenComp[2] + " " + fenComp[3]    

        board[y][x] = board[selected[0]][selected[1]]

        board[selected[0]][selected[1]] = EMPTY

        selected = None
        player = not player

    else:
        selected = None

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

board, allowed = parseFen("r3k2r/ppp2ppp/2nq1n2/2bppb2/2BPPB2/2NQ1N2/PPP2PPP/R3K2R  w KQkq - 0 1")

player = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    drawSquares(screen)
    player, board, allowed = parsemouse(board, player, allowed)
    drawPieces(screen, board, images)


    pygame.display.flip()
    clock.tick(60)