from typing import Optional
from random import choice
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
        empty_cells = []
        for x in range(self.state.board.size()):
            for y in range(self.state.board.size()):
                if self.state.board.get(Cell(x, y)) is None:
                    empty_cells.append(Cell(x, y))
        self.act_queue.append(Action.new_occupy(choice(empty_cells)))


class RandomActionQueue(ActionQueue):
    def __init__(self, random_ai: Random):
        self.random_ai = random_ai

    def pop(self) -> Optional[Action]:
        self.random_ai.act()
        if len(self.random_ai.act_queue) == 0:
            return None
        else:
            return self.random_ai.act_queue.pop()
