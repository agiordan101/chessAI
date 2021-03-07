import sys
sys.path.append('MCTS')

import MCTS_rave as mctsrd
from MCTS_rave import *
from chess_game import *

import time

n_game = 1
n_mcts_iter = 2000

def play_game():

	init_mcts()

	while True:

		i = 0
		begin_time = time.time()
		# for k in range(n_mcts_iter):
		while time.time() - begin_time < 3:
			reset_state()
			MCTS()
			i += 1
		print(f"MCTS turn {mctsrd.board.fullmove_number}\tnbr iter {i}\tw = {math.sqrt(len(list(mctsrd.board.legal_moves))) * 10}", file=sys.stderr, flush=True)

		reset_state()
		print_best_move()

		if mctsrd.board.is_game_over(claim_draw=True):
			result = mctsrd.board.result()
			print(f"Result: {result}")
			return result.split('-'), (chess.WHITE if result[:1] == "1-" else (chess.BLACK if result[:1] == "0-" else None))


winners = []
points = [0, 0]
for i in range(n_game):
	results = play_game()

	winners.append(results[1])
	points = [points[0] + float(results[0][0]), points[1] + float(results[0][1])]

print(f"{n_game} games:")
print(f"Points:  {points}")
print(f"Winners: {winners}")
