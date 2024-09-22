from settings import *
from helper import set_bit, clear_bit

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
    type = board[piece[0]][piece[1]]
    type = clear_bit(type, 3)
    type = clear_bit(type, 4)

    color = (board[piece[0]][piece[1]] >> 3) - 1
    
    recursive = not (type in [KNIGHT, KING])

    if type == PAWN:
        return GetPawnMoves(board, piece)

    moveoffset = directions[type]
    moves = []

    for move in moveoffset:
        if recursive:
            while True:
                field = [piece[0] + move[1], piece[1] + move[1]]
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
            field = [piece[0] + move[1], piece[1] + move[1]]
            fcolor = (board[field[0]][piece[1]] >> 3) - 1

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
    type = board[piece[0]][piece[1]]
    type = clear_bit(type, 3)
    type = clear_bit(type, 4)

    color = (board[piece[0]][piece[1]] >> 3) - 1

    if color == 0: #white is the first bit
        moveoffset = directions[PAWN + WHITE]
    else:
        moveoffset = directions[PAWN + BLACK]

    for i, move in enumerate(moveoffset):
        field = [piece[0] + move[1], piece[1] + move[1]]
        fcolor = (board[piece[0]][piece[1]] >> 3) - 1
        if i == 0:
            pass



if __name__ == "__main__":
    print((PAWN + WHITE >> 3) - 1)
