import math
import random
# import time
import copy

from chess_game import *

Ns = {}     # Number of time a state has been visited
Nsa = {}    # Number of time a state / action pair has been visited
Pmcts = {}  # Number of points after taking a state / action pair
Qmcts = {}  # Quality of a state / action pair

Sa = {}     # Moves save -> key: (fen, last_move), value: moves

# Hyperparameters
c = math.sqrt(2)

# Game state
board = chess.Board()

# --- SELECTION ---
def select_best_move_id(fen, moves):

	# print(f"SELECTION nbr moves {len(moves)}")
	best_move = None
	best_UCB = -1000000
	random.shuffle(moves)

	for Nsaid in moves:
		
		# Compute UCB value of this state/move pair
		ucb = Qmcts[Nsaid] + c * math.sqrt(Ns[fen]) / (1 + Nsa[Nsaid])

		# Save the best
		if ucb > best_UCB:

			best_UCB = ucb
			best_move = Nsaid

	# DEBUUUUG
	if not best_move:
		print(f"GROS PROBLEME FRERO")
		exit(0)

	return best_move, best_move[1]


# --- EXPANSION ---
def expansion(fen, moves):

	# print(f"EXPANSION")
	Ns[fen] = 1

	for Nsaid in moves:
		Nsa[Nsaid] = 0
		Pmcts[Nsaid] = 0
		Qmcts[Nsaid] = 0 # Useless ??


# --- SIMULATION ---
def simulation():

	# Get possible moves
	moves = get_moves_id(state, state.fen())

	# Draw case
	if not moves:
		# print(f"SIMULATION END DRAW")
		return 0

	# Select one randomly
	move = random.choice(moves)[1]
	
	# Apply move
	apply_move(state, move)

	return 1 if state.is_game_over() else simulation()

# --- Monte Carlo Tree Search (Rave optimisation) ---
def MCTS(depth=0):

	# fen is a unique string representing a state of the game
	fen = state.fen()

	# moves: [(fen, move0), ..., (fen, moveN)]
	moves = get_moves_id(state, fen)
	# print(f"Moves:\n{moves}")
	# print(f"Move 0: {str(moves[0])} type {type(moves[0])}")

	# At least 1 move exist ?
	if moves:

		# Node already exist ? -> Go deeper
		if fen in Ns:

			# - SELECTION
			best_move_id, best_move = select_best_move_id(fen, moves)

			apply_move(state, best_move)

			points = 1 if state.is_game_over() else MCTS(depth + 1)
			# print(f"BACKPROPAGATION depth {depth} / points {points}")
			
			# --- BACKPROPAGATION ---
			Ns[fen] += 1
			Nsa[best_move_id] += 1
			Pmcts[best_move_id] += points
			Qmcts[best_move_id] = Pmcts[best_move_id] / Nsa[best_move_id]
			return -points

		# -> Leaf node
		else:
			# print(f"if False")

			# - EXPENSION
			expansion(fen, moves)

			# print(f"SIMULATION ->")

			# - SIMULATION / CNN
			return -heuristic(state)

	# -> Draw
	else:
		return 0




# ----- MAIN FUNCTIONS -----

def print_best_move():
	
	moves = get_moves_id(board, board.fen())

	best_move = None
	best_value = -1000000
	for Nsaid in moves:

		print(f"Possible move -> {Nsaid[1]}: {Qmcts[Nsaid]}\t= {Pmcts[Nsaid]}\t/ {Nsa[Nsaid]}")

		if Qmcts[Nsaid] > best_value:
			best_move = Nsaid[1]
			best_value = Qmcts[Nsaid]

	if best_move:
		print(f"Apply my move -> {best_move}")
		apply_move(board, best_move)
		print_board(board)

	else:
		print(f"[ERROR MCTS RAVE] NO BEST VALUE")
		print(f"Nbr moves {len(moves)}")
		exit(1)


def reset_state():

	global state
	# state = copy.deepcopy(board)
	state = board.copy()

def init_mcts():

	print("-- INIT mcts / game --")
	global Ns
	global Nsa
	global Pmcts
	global Qmcts
	global Sa
	Ns = {}
	Nsa = {}
	Pmcts = {}
	Qmcts = {}
	Sa = {}

	global board
	board = chess.Board()
	reset_state()

	print_board(board)
