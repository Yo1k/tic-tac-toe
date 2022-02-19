from typing import Optional
from random import randrange
from yo1k.tic_tac_toe.kernel.game import (
    ActionQueue,
    Action,
    PlayerID,
    State,
    Phase,
    Cell)


class Random:
    def __init__(self, player_id: PlayerID, state: State):
        self.player_id = player_id
        self.state = state
        # self.seed = seed
        self.act_queue = []

    def act(self):
        if self.state.phase is Phase.BEGINNING \
                or self.state.phase is Phase.OUTROUND:
            self.act_beginning_outround()
        elif self.state.phase is Phase.INROUND:
            self.act_inround()
        else:
            assert False

    def act_beginning_outround(self):
        if self.player_id in self.state.required_ready:
            self.act_queue.append(Action.new_ready())

    def act_inround(self):
        empty_cells_cnt = self.state.board.size() ** 2 - self.state.step
        shift = randrange(empty_cells_cnt)
        for x in range(self.state.board.size()):
            for y in range(self.state.board.size()):
                if self.state.board.get(Cell(x, y)) is None:
                    if shift == 0:
                        self.act_queue.append(Action.new_occupy(Cell(x, y)))
                        break
                    shift -= 1


class RandomActionQueue(ActionQueue):
    def __init__(self, random_ai: Random):
        self.random_ai = random_ai

    def player_id(self) -> PlayerID:
        return self.random_ai.player_id

    def pop(self) -> Optional[Action]:
        self.random_ai.act()
        if len(self.random_ai.act_queue) == 0:
            return None
        else:
            return self.random_ai.act_queue.pop()
