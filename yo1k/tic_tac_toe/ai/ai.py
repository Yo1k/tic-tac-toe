from typing import Optional
from random import choice
from yo1k.tic_tac_toe.kernel.game import (
    ActionQueue,
    Action,
    Player,
    State,
    Phase,
    Cell)


class Random:
    def __init__(self, player: Player, state: State, seed: int):
        self.player = player
        self.state = state
        self.seed = seed
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
        player_idx = self.state.turn()
        if player_idx in self.state.required_ready:
            self.act_queue.append(Action.new_ready())

    def act_inround(self):
        empty_cells = []
        for x in range(self.state.board.size()):
            for y in range(self.state.board.size()):
                if self.state.board.get(Cell(x, y)) is None:
                    empty_cells.append(Cell(x, y))
        self.act_queue.append(Action.new_occupy(choice(empty_cells)))


class ActionQueueRandom(ActionQueue):
    def __init__(self, random_ai: Random):
        self.random_ai = random_ai

    def pop(self) -> Optional[Action]:
        self.random_ai.act()
        return self.random_ai.act_queue.pop()
