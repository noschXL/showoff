import time
from settings import *
from functools import wraps

def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)


def parseFen(notation: str):
    rowsizes = []
    needed_fields = 0

    for char in notation:
        if char == " ":
            break
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
    for i, char in enumerate(notation):
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
        elif char == " ":
            break
        else:
            colum += int(char)

    special = notation[i + 3:]

    player = notation[i + 1] == "w"

    return board, special, player

def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"running: {func.__name__}")
        start = time.time()
        output = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start}s to complete")
        return output
    
    return wrapper

def MoveTo(board: list[list[int]], new, old, allowed):

    y, x = new[0], new[1]

    type = board[old[0]][old[1]]
    color = type >> 3
    type = clear_bit(type, 3)
    type = clear_bit(type, 4)

    fenComp = allowed.split()

    toReml = ""

    if board[0][0] != ROOK + BLACK:
        toReml += "q"
    if board[0][7] != ROOK + BLACK:
        toReml += "k"
    if board[7][0] != ROOK + WHITE:
        toReml += "Q"
    if board[7][7] != ROOK + WHITE:
        toReml += "K"

    if type == KING:
        if color == 1:
            if old[1] - x == 2:    #queenside
                board[y][x + 1] = board[y][0]
                board[y][0] = EMPTY
            elif old[1] - x == -2: #kingside
                board[y][x - 1] = board[y][7]
                board[y][7] = EMPTY
            toReml += "KQ"
        elif color == 2:
            if old[1] - x == 2:    #queenside
                board[y][x + 1] = board[y][0]
                board[y][0] = EMPTY
            elif old[1] - x == -2: #kingside
                board[y][x - 1] = board[y][7]
                board[y][7] = EMPTY
            toReml += "kq"

    if toReml is not None:
        for toRem in toReml:
            fenComp[0] = fenComp[0].replace(toRem, "")

        if len(fenComp[0]) == EMPTY:
                fenComp[0] = "-"

    if type == PAWN:
        if fenComp[1] != "-":
            if [int(fenComp[1][1]), BOTTOMLETTERS.index(fenComp[1][0])] == [y,x]:
                if color == 1:     #white
                    board[y + 1][x] = EMPTY
                elif color == 2:   #black
                    board[y + 1][x] = EMPTY

    fenComp[1] = "-"
    if type == PAWN:
        if color == 1 and abs(old[0] - y) == 2: #white
            fenComp[1] = BOTTOMLETTERS[x] + str(y + 1)
        elif color == 2 and abs(old[0] - y) == 2: #black
            fenComp[1] = BOTTOMLETTERS[x] + str(y - 1)

    allowed = fenComp[0] + " " + fenComp[1] + " " + fenComp[2] + " " + fenComp[3]   

    board[y][x] = board[old[0]][old[1]]

    board[old[0]][old[1]] = EMPTY


    return board, allowed