from __future__ import annotations
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
        return (
            f"{type(self)}("
            f"mark={self.__mark},"
            f"wins={self.__wins})")


class Phase(Enum):
    BEGINNING = auto()
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
        return (
            f"{type(self)}("
            f"x={self.__x},"
            f"y={self.__y})")


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
        return (
            f"{type(self)}("
            f"cells={self.__cells},")


class State:
    """Full game state which is enough to restore a saved game."""

    def __init__(self,
                 game_rounds: int,
                 players: Sequence[Player],
                 board: Board,
                 phase=Phase.BEGINNING,
                 round_: int = 0,
                 step: int = 0):
        self.game_rounds = game_rounds
        self.round = round_
        assert len(players) == 2, f"{players}"
        self.players = players
        self.step = step
        self.phase = phase
        self.board = board

    def __str__(self):
        return (
            f"{type(self)}("
            f"game_rounds={self.game_rounds},"
            f"round={self.round},"
            f"players={self.players},"
            f"step={self.step},"
            f"phase={self.phase},"
            f"board={self.board})")


class Action:
    def __init__(self, surrender: bool, occupy: Optional[Cell], next_round: bool):
        assert (surrender is True and occupy is None and next_round is False) or \
               (surrender is False and occupy is not None and next_round is False) or \
               (surrender is False and occupy is None and next_round is True), (
            f"surrender={surrender}, occupy={occupy}, next_round={next_round}")
        self.__surrender = surrender
        self.__occupy = occupy
        self.__start = next_round

    @staticmethod
    def new_surrender() -> Action:
        return Action(True, None, False)

    @staticmethod
    def new_occupy(cell: Cell) -> Action:
        return Action(False, cell, False)

    @staticmethod
    def new_start() -> Action:
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
            action = f"occupy={self.__occupy}"
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
        assert len(action_queues) == 2, f"{action_queues}"
        self.__action_queues = action_queues

    def advance(self, state: State):
        turn = Logic.__turn(state)
        action = self.__action_queues[turn].next()
        if action is None:
            return None
        elif action.start is True:
            Logic.__start(state)
        elif action.surrender is True:
            Logic.__surrender(state)
        elif action.occupy is not None:
            Logic.__occupy(state, action.occupy)
        else:
            assert False

    @staticmethod
    def __turn(state: State) -> int:
        """Returns `turn` - the index of the current `Player` in `State.players`.

        `turn` is calculated in such a way as to alternate players order in different
        `round` while keeping the same `Player` index in the `State.players`.
        """
        return (state.step + state.round) % 2

    @staticmethod
    def __occupy(state: State, cell: Cell):
        assert state.phase is Phase.INROUND
        turn = Logic.__turn(state)
        mark = state.players[turn].mark()
        if state.board._get(cell) is None:
            state.board._set(cell, mark)
        else:
            assert False
        if Logic._win_condition(state.board, cell):
            Logic.__win(state)
        elif Logic.__last_step(state.step):
            Logic.__draw(state)
        else:
            state.step += 1

    @staticmethod
    def _win_condition(board: Board, last_occupied: Cell) -> bool:
        h_match = 0
        v_match = 0
        d1_match = 0
        d2_match = 0
        x = last_occupied.x
        y = last_occupied.y
        mark = board._get(last_occupied)
        for i in range(Board.size()):
            if board._get(Cell(i, y)) == mark:
                h_match += 1
            if board._get(Cell(x, i)) == mark:
                v_match += 1
            if board._get((Cell(i, i))) == mark:
                d1_match += 1
            if board._get(Cell(i, Board.size() - 1 - i)) == mark:
                d2_match += 1
        return (
            h_match == Board.size() or v_match == Board.size() or
            d1_match == Board.size() or d2_match == Board.size())

    @staticmethod
    def __last_step(step: int) -> bool:
        return step == Board.size() ** 2 - 1

    @staticmethod
    def __surrender(state: State):
        assert state.phase is Phase.INROUND
        idx_other_player = (Logic.__turn(state) + 1) % 2
        state.players[idx_other_player].wins += 1
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
        assert state.phase is Phase.BEGINNING or state.phase is Phase.OUTROUND
        if state.phase is Phase.OUTROUND:
            state.round += 1
            state.step = 0
            state.board._clean()
        elif state.phase is Phase.BEGINNING:
            pass
        else:
            assert False
        state.phase = Phase.INROUND

    def __str__(self):
        return (
            f"{type(self)}("
            f"action_queues={self.__action_queues})")


class World:
    def __init__(self, state: State, logic: Logic):
        self.__state = state
        self.__logic = logic

    def advance(self):
        self.__logic.advance(self.__state)

    def __str__(self):
        return (
            f"{type(self)}("
            f"state={self.__state},"
            f"logic={self.__logic})")
