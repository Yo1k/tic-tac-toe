from enum import Enum, auto
from collections.abc import Sequence
from typing import Optional
from abc import ABC, abstractmethod


class Mark(Enum):
    X = auto()
    O = auto()


class Player:
    def __init__(self, mark: Mark):
        self.__mark = mark
        self.__wins = 0

    def mark(self) -> Mark:
        return self.__mark

    @property
    def wins(self) -> int:
        return self.__wins

    @wins.setter
    def wins(self, wins: int):
        self.__wins = wins

    def __str__(self):
        return f"{type(self)}(" \
               f"mark={self.__mark}," \
               f"wins={self.__wins})"


class Phase(Enum):
    ONSET = auto()
    INROUND = auto()
    OUTROUND = auto()


class Cell:
    """A game board cell."""

    def __init__(self, x: int, y: int):
        assert 0 <= x < Board.size(), f"{x}"
        assert 0 <= y < Board.size(), f"{y}"
        self.__x = x
        self.__y = y

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    def __str__(self):
        return f"{type(self)}(" \
               f"x={self.__x}," \
               f"y={self.__y})"


class Board:
    def __init__(self, cells: Sequence[list[Optional[Mark]]] = None):
        self.__cells = Board.__empty_cells() if cells is None else cells

    def _set(self, cell: Cell, mark: Mark):
        self.__cells[cell.x][cell.y] = mark

    def _get(self, cell: Cell) -> Optional[Mark]:
        return self.__cells[cell.x][cell.y]

    def _clean(self):
        self.__cells = Board.__empty_cells()

    @property
    def cells(self):
        return self.__cells

    @staticmethod
    def size() -> int:
        return 3

    @staticmethod
    def __empty_cells() -> list[list[Optional[Mark]]]:
        return [[None for _ in range(Board.size())] for _ in range(Board.size())]

    def __str__(self):
        return f"{type(self)}(" \
               f"cells={self.__cells},"


class State:
    """Full game state which is enough to restore a paused game."""

    def __init__(self,
                 game_rounds: int,
                 players: Sequence[Player],
                 board: Board,
                 phase=Phase.ONSET,
                 cur_round: int = 0,
                 step: int = 0):
        self.game_rounds = game_rounds
        self.round = cur_round
        self.players = players
        self.step = step
        self.phase = phase
        self.board = board

    def __str__(self):
        return f"{type(self)}(" \
               f"game_rounds={self.game_rounds}," \
               f"round={self.round}," \
               f"players={self.players}," \
               f"step={self.step}," \
               f"phase={self.phase}," \
               f"board={self.board})"


class Action:
    def __init__(self, surrender: bool, occupy: Optional[Cell], next_round: bool):
        assert (surrender is True and occupy is None and next_round is False) or \
               (surrender is False and occupy is not None and next_round is False) or \
               (surrender is False and occupy is None and next_round is True)
        self.__surrender = surrender
        self.__occupy = occupy
        self.__start = next_round

    @staticmethod
    def new_surrender() -> "Action":
        return Action(True, None, False)

    @staticmethod
    def new_occupy(occupy: Cell) -> "Action":
        return Action(False, occupy, False)

    @staticmethod
    def new_start():
        return Action(False, None, True)

    @property
    def surrender(self):
        return self.__surrender

    @property
    def occupy(self):
        return self.__occupy

    @property
    def start(self):
        return self.__start

    def __str__(self):
        if self.__surrender is True:
            action = "surrender"
        elif self.__occupy is not None:
            action = f"new_occupy={self.__occupy}"
        elif self.__start is True:
            action = "start"
        else:
            assert False
        return f"{type(self)}(" \
               f"{action})"


class ActionQueue(ABC):
    @abstractmethod
    def next(self) -> Optional[Action]:
        pass


class Logic:
    """Game logic."""

    def __init__(self, action_queues: Sequence[ActionQueue]):
        """Indexes in `action_queues` correspond to indexes in `State.players`."""
        self.__action_queues = action_queues

    def advance(self, state: State):
        turn = Logic.__turn(state)
        action = self.__action_queues[turn].next()
        if action is None:
            return None
        elif action.start is True:
            assert state.phase is Phase.ONSET or state.phase is Phase.OUTROUND
            Logic.__start(state)
        elif action.surrender is True:
            assert state.phase is Phase.INROUND
            Logic.__surrender(state)
        elif action.occupy is not None:
            assert state.phase is Phase.INROUND
            Logic.__occupy(state, action.occupy)
        else:
            assert False

    @staticmethod
    def __turn(state: State) -> int:
        """Returns `turn` - the index of the current `Player` in `State.players`.

        `turn` is calculated in such a way as to alternate players order in different
        `round` keeping the same `Player` index in the `State.players`.
        """
        return (state.step + state.round) % 2

    @staticmethod
    def __occupy(state: State, cell: Cell):
        turn = Logic.__turn(state)
        mark = state.players[turn].mark()
        if state.board._get(cell) is None:
            state.board._set(cell, mark)
        else:
            pass
        if Logic._win_condition(state.board, cell):
            Logic.__win(state)
        elif Logic._draw_condition(state.step):
            Logic.__draw(state)
        else:
            state.step += 1

    @staticmethod
    def _win_condition(board: Board, cell: Cell) -> bool:
        win_condition = False
        horizontal_match_number = 0
        vertical_match_number = 0
        first_diagonal_match_number = 0
        second_diagonal_match_number = 0
        x = cell.x
        y = cell.y
        mark = board._get(Cell(x, y))
        for i in range(Board.size()):
            if board._get(Cell(i, y)) == mark:
                horizontal_match_number += 1
            if board._get(Cell(x, i)) == mark:
                vertical_match_number += 1
            if board._get((Cell(i, i))) == mark:
                first_diagonal_match_number += 1
            if board._get(Cell(i, Board.size() - 1 - i)) == mark:
                second_diagonal_match_number += 1
        if horizontal_match_number == Board.size() or \
           vertical_match_number == Board.size() or \
           first_diagonal_match_number == Board.size() or \
           second_diagonal_match_number == Board.size():
            win_condition = True
        return win_condition

    @staticmethod
    def _draw_condition(step: int) -> bool:
        draw_condition = False
        if step == Board.size() ** 2 - 1:
            draw_condition = True
        return draw_condition

    @staticmethod
    def __surrender(state: State):
        index_other_player = (Logic.__turn(state) + 1) % 2
        state.players[index_other_player].wins += 1
        state.phase = Phase.OUTROUND

    @staticmethod
    def __win(state: State):
        state.players[Logic.__turn(state)].wins += 1
        state.phase = Phase.OUTROUND

    @staticmethod
    def __draw(state: State):
        state.phase = Phase.OUTROUND

    @staticmethod
    def __start(state: State):
        if state.phase is Phase.OUTROUND:
            state.round += 1
            state.step = 0
            state.board._clean()
        elif state.phase is Phase.ONSET:
            pass
        else:
            assert False
        state.phase = Phase.INROUND

    def __str__(self):
        return f"{type(self)}(" \
               f"action_queues={self.__action_queues})"


class World:
    def __init__(self, state: State, logic: Logic):
        self.__state = state
        self.__logic = logic

    def run(self):  # SKTODO make method
        pass

    def __str__(self):
        return f"{type(self)}(" \
               f"state={self.__state}," \
               f"logic={self.__logic})"
