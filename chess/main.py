import sys
import pygame
import os
from math import floor

path = os.path.abspath(os.path.dirname(__file__))

EMPTY = 0
PAWN = 1
BISHOP = 2
KNIGHT = 3
ROOK = 4
QUEEN = 5
KING = 6

WHITE = 0
BLACK = 1

WHITECOLOR = "#d0a465"
BLACKCOLOR = "#5d421c"

lastInput = False

selected = None  # always None or [x,y] of the board location

clock = pygame.time.Clock()


class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except e:
            print(f'Unable to load spritesheet image: {filename} due to {e}')

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None, mult_size = 2):
        "Loads multiple images, supply a list of coordinates"
        imglist = []
        for rect in rects:
            image = self.image_at(rect, colorkey)
            image = pygame.transform.scale_by(image, mult_size)
            imglist.append(image)
        return imglist

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
            board[row][colum] = PAWN + 6 * int(char.lower() == char)
            colum += 1
        elif char.lower() == "b":
            board[row][colum] = BISHOP + 6 * int(char.lower() == char)
            colum += 1
        elif char.lower() == "n":
            board[row][colum] = KNIGHT + 6 * int(char.lower() == char)
            colum += 1
        elif char.lower() == "r":
            board[row][colum] = ROOK + 6 * int(char.lower() == char)
            colum += 1
        elif char.lower() == "q":
            board[row][colum] = QUEEN + 6 * int(char.lower() == char)
            colum += 1
        elif char.lower() == "k":
            board[row][colum] = KING + 6 * int(char.lower() == char)
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

    if  (selected is None and board[y][x] // 7 != player) or (board[y][x] != EMPTY and board[y][x] // 7 != player and not [x,y] == selected):  #TODO: make it cleaner

        selected = [x,y]

    elif selected is not None and [x,y] != selected and (board[y][x] == EMPTY or board[y][x] // 7 == player):
        print(1)
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
                screen.blit(images[board[y][x] - 1], (x * 70 + 3, y * 70 + 3)) # draw the image, 70 x 70 square, 64 x 64 sprite, 3 px edge

def get_moves(board: list[list[int]], piece: list[int,int]):
    piece_id = board[piece[1]][piece[0]]
    piece_id = (piece_id + 1) % 7
    print(piece_id)

screen = pygame.display.set_mode((70 * 8, 70 * 8))

whiteSpriteSheet = spritesheet(os.path.join(path, "pieces_white.png"))
blackSpriteSheet = spritesheet(os.path.join(path, "pieces_black.png"))

imgrects = [(x * 32,0,32,32) for x in range(6)]
images = [] + whiteSpriteSheet.images_at(imgrects, (255,0,0))
images += blackSpriteSheet.images_at(imgrects, (255,0,0))

board = parseFen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

player = True

get_moves(board, [1,0])

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