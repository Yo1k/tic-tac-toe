from collections import deque
from typing import Optional

from yo1k.tic_tac_toe.kernel.game import ActionQueue, Action


class DefaultActionQueue(ActionQueue):
    def __init__(self) -> None:
        self.actions: deque[Action] = deque()

    def add(self, action: Action) -> None:
        self.actions.append(action)

    def pop(self) -> Optional[Action]:
        if len(self.actions) == 0:
            return None
        else:
            return self.actions.popleft()
