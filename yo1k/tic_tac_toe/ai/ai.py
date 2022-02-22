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
        self.__player_id: PlayerID = player_id
        self.__rng: Random = Random(seed)
        self.__action_queue: DefaultActionQueue = action_queue

    def act(self, state: State) -> None:
        if state.phase is Phase.BEGINNING \
                or state.phase is Phase.OUTROUND:
            self.__act_beginning_outround(state)
        elif state.phase is Phase.INROUND:
            self.__act_inround(state)
        else:
            assert False

    def __act_beginning_outround(self, state: State) -> None:
        if self.__player_id in state.required_ready:
            self.__action_queue.add(Action.new_ready())

    def __act_inround(self, state: State) -> None:
        if self.__player_id != state.turn():
            return
        empty_cells_cnt = state.board.size() ** 2 - state.step
        shift = self.__rng.randrange(empty_cells_cnt)
        for x in range(state.board.size()):
            for y in range(state.board.size()):
                cell = Cell(x, y)
                if state.board.get(cell) is None:
                    if shift == 0:
                        self.__action_queue.add(Action.new_occupy(cell))
                        return
                    shift -= 1

    def __repr__(self) -> str:
        return (f"{type(self).__qualname__}("
                f"player_id={self.__player_id},"
                f"action_queue={self.__action_queue})")
