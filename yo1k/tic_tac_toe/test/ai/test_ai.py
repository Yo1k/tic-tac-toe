import unittest
from typing import Optional

from yo1k.tic_tac_toe.kernel.game import (State, Player, Board, Phase, PlayerID, Mark, Logic)
from yo1k.tic_tac_toe.ai.ai import Random, RandomActionQueue


def _new_state(
        game_rounds: int = 5,
        player_x: Optional[Player] = None,
        player_o: Optional[Player] = None,
        board: Optional[Board] = None,
        phase: Phase = Phase.INROUND,
        round_: int = 0,
        step: int = 0,
        required_ready: Optional[set[PlayerID]] = None) -> State:
    player_x = Player(Mark.X, PlayerID(0)) if player_x is None else player_x
    player_o = Player(Mark.O, PlayerID(1)) if player_o is None else player_o
    board = Board() if board is None else board
    required_ready = set() if required_ready is None else required_ready
    return State(
            game_rounds=game_rounds, players=(player_x, player_o), board=board, phase=phase,
            round_=round_, step=step, required_ready=required_ready)


class RandomAITest(unittest.TestCase):
    def test_something(self):
        state = _new_state()
        random_ai = Random(PlayerID(0), state)
        act_queue_px = RandomActionQueue(random_ai)
        self.assertEqual(True, False)


if __name__ == '__main__':
    # unittest.main()
    player_x = Player(Mark.X, PlayerID(0))
    player_o = Player(Mark.O, PlayerID(1))
    state = State(
            game_rounds=5,
            board=Board(),
            players=(player_x, player_o))
    random_ai_x = Random(player_x.id, state)
    random_ai_o = Random(player_o.id, state)
    act_queue_px = RandomActionQueue(random_ai_x)
    act_queue_po = RandomActionQueue(random_ai_o)
    logic = Logic((act_queue_px, act_queue_po))
    while state.round <= 20:
        logic.advance(state)
        if state.phase is Phase.OUTROUND:
            print(f"round {state.round}")
            print(state.board)
            print(f"pl_x: {state.players[0].wins}, pl_o: {state.players[1].wins}", end="\n\n")
