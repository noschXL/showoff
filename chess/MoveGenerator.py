from settings import *
from helper import clear_bit, timed, MoveTo
from copy import deepcopy

directions = { PAWN + WHITE: [[-1, 0], [-2, 0], [-1, 1], [-1, -1]],
               PAWN + BLACK: [[1, 0], [2, 0], [1, 1], [1, -1]],
              
               BISHOP: [[-1,-1], [-1, 1], [1, 1], [1,-1]],
              
               KNIGHT: [[-2, 1], [-2,-1], [-1, 2], [-1,-2],
                        [2, 1], [2,-1], [1, 2], [1, -2]],

               ROOK: [[-1, 0], [1, 0], [0, -1], [0, 1]],

               QUEEN: [[-1,-1], [-1, 1], [1, 1], [1,-1],
                       [-1, 0], [1, 0], [0, -1], [0, 1]],

               KING: [[-1,-1], [-1, 1], [1, 1], [1,-1],
                       [-1, 0], [1, 0], [0, -1], [0, 1]]
               }

def GetPseudoMoves(board: list[list[int]], piece: list[int], allowed: str) -> list[list[int]]: #returns a list of possible move coords
    type = board[piece[0]][piece[1]]
    color = type >> 3
    type = clear_bit(type, 3)
    type = clear_bit(type, 4)
   
    recursive = not (type in [KNIGHT, KING])

    if type == PAWN:
        return GetPawnMoves(board, piece, allowed)

    moveoffset = directions[type]
    moves = []

    for move in moveoffset:
        if recursive:
            field = [piece[0] + move[0], piece[1] + move[1]]
            while True:

                if (field[0] < 0) or (field[0] > 7) or (field[1] < 0) or (field[1] > 7):
                    break
                fcolor = (board[field[0]][field[1]] >> 3)

                if fcolor == EMPTY:
                    moves.append(field)
                elif fcolor == color:
                    break
                elif fcolor != color:
                    moves.append(field)
                    break
                else:
                    raise ValueError("idk whats wrong")
                
                field = [field[0] + move[0], field[1] + move[1]]
# ---------------------------------------------------------------  
        else:
            field = [piece[0] + move[0], piece[1] + move[1]]
            if (field[0] < 0) or (field[0] > 7) or (field[1] < 0) or (field[1] > 7):
                continue
            fcolor = (board[field[0]][field[1]] >> 3)

            if fcolor == EMPTY:
                moves.append(field)
            elif fcolor == color:
                continue
            elif fcolor != color:
                moves.append(field)
                continue
            else:
                raise ValueError("idk whats wrong")

    if type == KING:
        if color == 1:
            if "K" in allowed:
                field = [piece[0], piece[1] + 1]
                fcolor = (board[field[0]][field[1]] >> 3)
                if fcolor == EMPTY:
                    field = [piece[0], piece[1] + 2]
                    fcolor = (board[field[0]][field[1]] >> 3)    
                    if fcolor == EMPTY:
                        moves.append(field)

            if "Q" in allowed:
                field = [piece[0], piece[1] - 1]
                fcolor = (board[field[0]][field[1]] >> 3)
                if fcolor == EMPTY:
                    field = [piece[0], piece[1] - 2]
                    fcolor = (board[field[0]][field[1]] >> 3)    
                    if fcolor == EMPTY:
                        field2 = [piece[0], piece[1] - 3]
                        fcolor2 = (board[field2[0]][field2[1]] >> 3)    
                        if fcolor2 == EMPTY:
                            moves.append(field)

        else:
            if "k" in allowed:
                field = [piece[0], piece[1] + 1]
                fcolor = (board[field[0]][field[1]] >> 3)
                if fcolor == EMPTY:
                    field = [piece[0], piece[1] + 2]
                    fcolor = (board[field[0]][field[1]] >> 3)    
                    if fcolor == EMPTY:
                        moves.append(field)

            if "q" in allowed:
                field = [piece[0], piece[1] - 1]
                fcolor = (board[field[0]][field[1]] >> 3)
                if fcolor == EMPTY:
                    field = [piece[0], piece[1] - 2]
                    fcolor = (board[field[0]][field[1]] >> 3)    
                    if fcolor == EMPTY:
                        field2 = [piece[0], piece[1] - 3]
                        fcolor2 = (board[field2[0]][field2[1]] >> 3)    
                        if fcolor2 == EMPTY:
                            moves.append(field)

    return moves

def GetPawnMoves(board: list[list[int]], piece: list[int], allowed: str) -> list[list[int]]: # -n-
    type = board[piece[0]][piece[1]]
    type = clear_bit(type, 3)
    type = clear_bit(type, 4)

    color = (board[piece[0]][piece[1]] >> 3)

    moves = []

    if color == 1: #* white is the first bit
        moveoffset = directions[PAWN + WHITE]
    else:
        moveoffset = directions[PAWN + BLACK]

    for i, move in enumerate(moveoffset):
        field = [piece[0] + move[0], piece[1] + move[1]]
        if (field[0] < 0) or (field[0] > 7) or (field[1] < 0) or (field[1] > 7):
            continue
        fcolor = (board[field[0]][field[1]] >> 3)

        if i == 0: #* one forward
            if fcolor == EMPTY:
                moves.append(field)
            elif fcolor == color:
                continue
            elif fcolor != color:
                continue
            else:
                raise ValueError("idk whats wrong")
            
        elif i == 1: #* 2 forward
            if len(moves) != 0 and fcolor == EMPTY and ((color == 2 and piece[0] == 1) or (color == 1 and piece[0] == 6)):
                moves.append(field)
            elif fcolor == color:
                continue
            elif fcolor != color:
                continue
            else:
                raise ValueError("idk whats wrong")
            
        elif i == 2 or i == 3:

            fenComp = allowed.split()[1]

            canPassant = False

            if fenComp != "-":
                if [int(fenComp[1]), BOTTOMLETTERS.index(fenComp[0])] == field:

                    canPassant = True
            if canPassant:
                moves.append(field)
            elif fcolor == EMPTY:
                continue
            elif fcolor == color:
                continue
            elif fcolor != color:
                moves.append(field)
            else:
                raise ValueError("idk whats wrong")

    return moves

def GetAllPseudoMoves(board: list[list[int]], player: bool, allowed: str) -> list[list[int]]:
    color = 1 if player else 2

    moves = []

    for y, row in enumerate(board):
        for x, colum in enumerate(row):
            fcolor = (board[y][x] >> 3)
            if fcolor == color:
                moves += GetPseudoMoves(board, [y,x], allowed)

    return moves

def GetFirst(board: list[list[int]], piece: int) -> list[int]:
    for y, row in enumerate(board):
        for x, colum in enumerate(row):
            if colum == piece:
                return [y,x]

def Checked(board: list[list[int]], player: bool, allowed: str) -> bool:
    color = 1 if player else 2
    myKingPos = GetFirst(board, KING + (WHITE if color == 1 else BLACK))
    enemymoves = GetAllPseudoMoves(board, color == 2, allowed)
    return myKingPos in enemymoves

def GetLegalMoves(board: list[list[int]], piece: list[int], allowed: str) -> list[list[int]]: #returns a list of possible move coords
    pseudomoves = GetPseudoMoves(board, piece, allowed)
    color = (board[piece[0]][piece[1]] >> 3)

    legalmoves = []

    for move in pseudomoves:
        newboard, newallowed = MoveTo(deepcopy(board), move, piece, allowed)
        if not Checked(newboard, color == 1, newallowed):
            legalmoves.append(move)

    return legalmoves

def GetAllLegalMoves(board: list[list[int]], player: bool, allowed: str) -> list[list[int]]:
    color = 1 if player else 2

    moves = []

    for y, row in enumerate(board):
        for x, colum in enumerate(row):
            fcolor = (board[y][x] >> 3)
            if fcolor == color:
                moves += GetLegalMoves(board, [y,x], allowed)

    return moves

def Checkmated(board: list[list[int]], player: bool, allowed:str) -> bool:
    if Checked(board, player, allowed):
        return len(GetAllLegalMoves(board, player, allowed)) == 0

if __name__ == "__main__":
    print((PAWN + WHITE >> 3)) # 1
    print((PAWN + BLACK >> 3)) # 2
    print((EMPTY >> 3))        # 0
