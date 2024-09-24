from settings import *

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

    return board, special

