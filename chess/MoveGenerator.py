from settings import *
from helper import set_bit, clear_bit
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
def GetMoves(board: list[list[int]], piece: list[int]) -> list[list[int]]: #returns a list of possible move coords
    type = deepcopy(board[piece[0]][piece[1]])
    type = clear_bit(type, 3)
    type = clear_bit(type, 4)
    type += 0
    color = (board[piece[0]][piece[1]] >> 3) - 1
    
    recursive = not (type in [KNIGHT, KING])

    if type == PAWN:
        return GetPawnMoves(board, piece)

    moveoffset = directions[type]
    moves = []

    for move in moveoffset:
        if recursive:
            while True:
                field = [piece[0] + move[0], piece[1] + move[1]]
                if (field[0] < 0) or (field[0] > 7) or (field[1] < 0) or (field[1] > 7):
                    break
                fcolor = (board[field[0]][field[1]] >> 3) - 1

                if fcolor == -1:
                    moves.append(field)
                elif fcolor == color:
                    break
                elif fcolor != color:
                    moves.append(field)
                    break
                else:
                    raise ValueError("idk whats wrong")
                
        else:
            field = [piece[0] + move[0], piece[1] + move[1]]
            if (field[0] < 0) or (field[0] > 7) or (field[1] < 0) or (field[1] > 7):
                break
            fcolor = (board[field[0]][field[1]] >> 3) - 1

            if fcolor == -1:
                moves.append(field)
            elif fcolor == color:
                continue
            elif fcolor != color:
                moves.append(field)
                continue
            else:
                raise ValueError("idk whats wrong")
            
    return moves

def GetPawnMoves(board: list[list[int]], piece: list[int]) -> list[list[int]]: # -n-
    type = deepcopy(board[piece[0]][piece[1]])
    type = clear_bit(type, 3)
    type = clear_bit(type, 4)

    color = (board[piece[0]][piece[1]] >> 3) - 1

    moves = []

    if color == 0: #* white is the first bit
        moveoffset = directions[PAWN + WHITE]
    else:
        moveoffset = directions[PAWN + BLACK]

    for i, move in enumerate(moveoffset):
        field = [piece[0] + move[0], piece[1] + move[1]]
        if (field[0] < 0) or (field[0] > 7) or (field[1] < 0) or (field[1] > 7):
            break
        fcolor = (board[piece[0]][piece[1]] >> 3) - 1
        print(field, fcolor)

        if i == 0: #* one forward
            if fcolor == -1:
                moves.append(field)
            elif fcolor == color:
                continue
            elif fcolor != color:
                continue
            else:
                raise ValueError("idk whats wrong")
            
        elif i == 1: #* 2 forward
            if fcolor == -1 and (color == 1 and piece[0] == 1) or (color == 0 and piece[0] == 7):
                moves.append(field)
            elif fcolor == color:
                continue
            elif fcolor != color:
                continue
            else:
                raise ValueError("idk whats wrong")
            
        elif i == 2 or i == 3:
            if fcolor == -1:
                continue
            elif fcolor == color:
                continue
            elif fcolor != color:
                moves.append(field)
            else:
                raise ValueError("idk whats wrong")

    return moves

if __name__ == "__main__":
    print((PAWN + WHITE >> 3) - 1)
