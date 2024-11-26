from settings import *
from helper import clear_bit

def Evaluate(board: list[list[int]]) -> float:
	eval = 0
	for row in board:
		for piece in row:
			type = board[piece[0]][piece[1]]
			color = type >> 3
			type = clear_bit(type, 3)
			type = clear_bit(type, 4)

			if type == QUEEN:
				eval += (1 if color == 1 else -1) * QUEENVALUE
			elif type == ROOK:
				eval += (1 if color == 1 else -1) * ROOKVALUE
			elif type == BISHOP:
				eval += (1 if color == 1 else -1) * BISHOPVALUE
			elif type == KNIGHT:
				eval += (1 if color == 1 else -1) * KNIGHTVALUE
			elif type == PAWN:
				eval += (1 if color == 1 else -1) * PAWNVALUE

	return eval