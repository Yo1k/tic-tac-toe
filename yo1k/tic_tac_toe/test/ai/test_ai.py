import unittest
import sys
from random import randrange
from yo1k.tic_tac_toe.kernel.game import (
    State, Player, Board, PlayerID, Mark, Logic, World)
from yo1k.tic_tac_toe.ai.ai import RandomAI
from yo1k.tic_tac_toe.kernel.action_queue import DefaultActionQueue


class RandomAITest(unittest.TestCase):
    def test_play_against_itself(self) -> None:
        for _ in range(100):
            ai_rng_seed_px = randrange(sys.maxsize)
            ai_rng_seed_po = randrange(sys.maxsize)
            player_x = Player(PlayerID(0), Mark.X)
            player_o = Player(PlayerID(1), Mark.O)
            px_id = player_x.id
            po_id = player_o.id
            act_queue_px = DefaultActionQueue(px_id)
            act_queue_po = DefaultActionQueue(po_id)
            state = State(
                    game_rounds=5,
                    board=Board(),
                    players=(player_x, player_o))
            logic = Logic((act_queue_px, act_queue_po))
            ai_x = RandomAI(player_x.id, ai_rng_seed_px, act_queue_px)
            ai_o = RandomAI(player_o.id, ai_rng_seed_po, act_queue_po)
            world = World(state, logic, (ai_x, ai_o))
            possible_round_loops = (state.board.size() ** 2 + 1) * state.game_rounds
            for _ in range(possible_round_loops):
                world.advance()
            with self.subTest(ai_rng_seed_px=ai_rng_seed_px, ai_rng_seed_po=ai_rng_seed_po):
                self.assertIs(True, logic.is_game_over(state))


if __name__ == '__main__':
    unittest.main()
