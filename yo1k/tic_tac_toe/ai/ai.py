from random import randrange
from yo1k.tic_tac_toe.kernel.action_queue import DefaultActionQueue
from yo1k.tic_tac_toe.kernel.game import (
    Action,
    PlayerID,
    State,
    Phase,
    Cell)


class Random:
    def __init__(self, player_id: PlayerID, action_queue: DefaultActionQueue):
        self._player_id = player_id
        # self.seed = seed
        self.act_queue = action_queue

    def act_beginning_outround(self, state: State):
        if self._player_id in state.required_ready:
            self.act_queue.add(Action.new_ready())

    def act_inround(self, state: State):
        if self._player_id != state.turn():
            return
        empty_cells_cnt = state.board.size() ** 2 - state.step
        shift = randrange(empty_cells_cnt)
        for x in range(state.board.size()):
            for y in range(state.board.size()):
                if state.board.get(Cell(x, y)) is None:
                    if shift == 0:
                        self.act_queue.add(Action.new_occupy(Cell(x, y)))
                        return
                    shift -= 1


class AI:
    def __init__(self, random: Random):
        self.random: Random = random

    def act(self, state: State):
        if state.phase is Phase.BEGINNING \
                or state.phase is Phase.OUTROUND:
            self.random.act_beginning_outround(state)
        elif state.phase is Phase.INROUND:
            self.random.act_inround(state)
        else:
            assert False
