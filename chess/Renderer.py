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
