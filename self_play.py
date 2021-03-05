import sys
sys.path.append('MCTS')

import MCTS_rave as mctsrd
from MCTS_rave import *
from chess_game import *

n_game = 1
n_mcts_iter = 500

def play_game():

	init_mcts()

	while True:

		for k in range(n_mcts_iter):
			reset_state()
			MCTS()
		print(f"MCTS\tlast_move\tnbr iter {n_mcts_iter}", file=sys.stderr, flush=True)

		reset_state()
		print_best_move()

		if mctsrd.board.is_game_over():
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
