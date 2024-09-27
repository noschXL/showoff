import pygame
from settings import *
from helper import sizefactor

def drawSquares(screen: pygame.Surface):
    for x in range(8):
        for y in range(8):
            color = WHITECOLOR if (x+y) % 2 == 0 else BLACKCOLOR
            pygame.draw.rect(screen, color, (x * 70 * sizefactor, y * 70 * sizefactor, 70 * sizefactor, 70 * sizefactor))

def drawPieces(screen: pygame.Surface, board: list[list[int]], images: list[pygame.Surface]):
    for y in range(8): #down
        for x in range(8): #right
            if board[y][x] == EMPTY:
                pass
            else:
                screen.blit(images[board[y][x] - 1 - WHITE -  (2 if board[y][x] - WHITE >= 8 else 0)  ], (x * 70 * sizefactor,y * 70* sizefactor,70 * sizefactor,70 * sizefactor))

def drawMoveable(screen, moves: list[list[int]] | None = None):
    if moves is not None:
        for move in moves:
            pygame.draw.rect(screen, MOVEABLECOLOR, (move[1] * 70 * sizefactor, move[0] * 70 * sizefactor, 70 * sizefactor, 70 * sizefactor))

def drawSelected(screen, selected: list[int] | None = None):
    if selected is not None:
        pygame.draw.rect(screen, SELECTEDCOLOR, (selected[1] * 70 * sizefactor, selected[0] * 70 * sizefactor, 70 * sizefactor, 70 * sizefactor))

def drawBoard(screen, board, images):
    drawSquares(screen)
    drawPieces(screen, board, images)

def drawPromotion(screen: pygame.Surface, promoPos: list[int], images: list[pygame.Surface]):
    color = WHITE if promoPos[0] == 0 else BLACK
    rects = []
    if promoPos[0] == 0:
        for i in range(4):
            rect = pygame.Rect(promoPos[1] * 70 * sizefactor, (promoPos[0] + i) * 70 * sizefactor, 70 * sizefactor, 70 * sizefactor)
            rects.append(rect)
            pygame.draw.rect(screen, SELECTEDCOLOR, rect)
            screen.blit(images[PROMOSELECT[i] - 1], rect)
    else:
        for i in range(4):
            rect = pygame.Rect(promoPos[1] * 70 * sizefactor, 70 * 8 * sizefactor -((promoPos[0] + i) * 70 * sizefactor), 70 * sizefactor, 70 * sizefactor)
            pygame.draw.rect(screen, SELECTEDCOLOR, rect)
            screen.blit(images[PROMOSELECT[i] - 7], rect)
            rects.append(rect)

    return rects