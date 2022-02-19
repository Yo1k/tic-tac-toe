import unittest
from yo1k.tic_tac_toe.kernel.game import (
    State, Player, Board, PlayerID, Mark, Logic, World)
from yo1k.tic_tac_toe.ai.ai import Random, AI
from yo1k.tic_tac_toe.kernel.action_queue import DefaultActionQueue
import timeout_decorator
import time


class RandomAITest(unittest.TestCase):
    @timeout_decorator.timeout(0.3)
    def test_play_against_itself(self):
        player_x = Player(PlayerID(0), Mark.X)
        player_o = Player(PlayerID(1), Mark.O)
        state = State(
                game_rounds=5,
                board=Board(),
                players=(player_x, player_o))
        act_queue_px = DefaultActionQueue(state.players[0].id)
        act_queue_po = DefaultActionQueue(state.players[1].id)
        logic = Logic((act_queue_px, act_queue_po))
        ai_x = AI(Random(player_x.id, act_queue_px))
        ai_o = AI(Random(player_o.id, act_queue_po))
        world = World(state, logic, (ai_x, ai_o))
        start_runtime = time.time()
        while state.round <= 1000:
            world.advance()
        stop_runtime = time.time()
        print(f"Games lasted {(stop_runtime - start_runtime) * 1000} ms")
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
