from random import Random
from yo1k.tic_tac_toe.kernel.action_queue import DefaultActionQueue
from yo1k.tic_tac_toe.kernel.game import (
    Action,
    PlayerID,
    State,
    Phase,
    Cell,
    AI)


class RandomAI(AI):
    def __init__(self, player_id: PlayerID, seed: int, action_queue: DefaultActionQueue):
        self._player_id: PlayerID = player_id
        self._rng: Random = Random(seed)
        self._act_queue: DefaultActionQueue = action_queue

    def act(self, state: State) -> None:
        if state.phase is Phase.BEGINNING \
                or state.phase is Phase.OUTROUND:
            self.act_beginning_outround(state)
        elif state.phase is Phase.INROUND:
            self.act_inround(state)
        else:
            assert False

    def act_beginning_outround(self, state: State) -> None:
        if self._player_id in state.required_ready:
            self._act_queue.add(Action.new_ready())

    def act_inround(self, state: State) -> None:
        if self._player_id != state.turn():
            return
        empty_cells_cnt = state.board.size() ** 2 - state.step
        shift = self._rng.randrange(empty_cells_cnt)
        for x in range(state.board.size()):
            for y in range(state.board.size()):
                if state.board.get(Cell(x, y)) is None:
                    if shift == 0:
                        self._act_queue.add(Action.new_occupy(Cell(x, y)))
                        return
                    shift -= 1
