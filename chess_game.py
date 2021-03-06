import chess
import chess.svg
from chessboard import display
import math

piece_values = [(chess.PAWN, 1.0),
				(chess.KNIGHT, 3.2),
				(chess.BISHOP, 3.33),
				(chess.ROOK, 5.1),
				(chess.QUEEN, 8.8)]

def get_moves_id(board, fen):
	return [(fen, str(move)) for move in board.legal_moves]

def apply_move(board, move):
	board.push(chess.Move.from_uci(move))

def print_board(board):
	print(f"Board:\n{board}")
	display.start(board.fen())

def max_points(turn, n_moves):
	# return math.sqrt(turn) * n_moves
	return math.sqrt(n_moves) * 10

def heuristic(state, n_moves):

	baseBoard = chess.BaseBoard(state.fen().split()[0])

	my_score = 0
	opponent_score = 0

	my_color = state.turn
	opponent_color = not my_color

	for pieceType, value in piece_values:
		my_score += len(baseBoard.pieces(pieceType, my_color)) * value
		opponent_score += len(baseBoard.pieces(pieceType, opponent_color)) * value

	if my_score > opponent_score:
		points = 1 - opponent_score / my_score
	else:
		points = my_score / opponent_score - 1

	return points
	# return points * max_points(state.fullmove_number, n_moves)