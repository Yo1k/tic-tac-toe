from collections import deque
from typing import Optional

from yo1k.tic_tac_toe.kernel.game import ActionQueue, Action, PlayerID


class DefaultActionQueue(ActionQueue):
    def __init__(self, player_id: PlayerID) -> None:
        self.__player_id = player_id
        self.actions: deque[Action] = deque()

    def add(self, action: Action) -> None:
        self.actions.append(action)

    def player_id(self) -> PlayerID:
        return self.__player_id

    def pop(self) -> Optional[Action]:
        if len(self.actions) == 0:
            return None
        else:
            return self.actions.popleft()

    def __repr__(self) -> str:
        return (f"{type(self).__qualname__}("
                f"player_id={self.__player_id},"
                f"actions={self.actions})")
