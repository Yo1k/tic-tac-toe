from __future__ import annotations
from collections import deque
from collections.abc import Sequence, MutableSequence
from enum import Enum, auto
from typing import Optional
from abc import ABC, abstractmethod
from yo1k.tic_tac_toe.util import eq


class Mark(Enum):
    X = auto()
    O = auto()


@eq
class PlayerID:
    def __init__(self, idx: int):
        self.idx: int = idx

    def __repr__(self) -> str:
        return (f"{type(self).__qualname__}("
                f"idx={self.idx})")


@eq
class Player:
    def __init__(self, id_: PlayerID, mark: Mark):
        self.id: PlayerID = id_
        self.mark: Mark = mark
        self.wins: int = 0

    def __repr__(self) -> str:
        return (f"{type(self).__qualname__}("
                f"id={self.id},"
                f"mark={self.mark},"
                f"wins={self.wins})")


class Phase(Enum):
    BEGINNING = auto()
    INROUND = auto()
    OUTROUND = auto()


class Cell:
    """A game board cell."""

    def __init__(self, x: int, y: int):
        assert 0 <= x < Board.const_size(), f"{x}, {Board.const_size()}"
        assert 0 <= y < Board.const_size(), f"{y}, {Board.const_size()}"
        self.x: int = x
        self.y: int = y

    def __repr__(self) -> str:
        return (f"{type(self).__qualname__}("
                f"x={self.x},"
                f"y={self.y})")


@eq
class Board:
    def __init__(self, cells: Optional[Sequence[MutableSequence[Optional[Mark]]]] = None):
        self.cells: Sequence[MutableSequence[Optional[Mark]]] \
            = Board.__empty_cells() if cells is None else cells
        Board.__assert_board(self.cells, self.size())

    def set(self, cell: Cell, mark: Mark) -> None:
        assert self.cells[cell.x][cell.y] is None
        self.cells[cell.x][cell.y] = mark

    def get(self, cell: Cell) -> Optional[Mark]:
        return self.cells[cell.x][cell.y]

    def clear(self) -> None:
        for x in range(self.size()):
            for y in range(self.size()):
                self.cells[x][y] = None

    def size(self) -> int:
        return len(self.cells)

    @staticmethod
    def const_size() -> int:
        return 3

    @staticmethod
    def __empty_cells() -> Sequence[MutableSequence[Optional[Mark]]]:
        return [[None for _ in range(Board.const_size())] for _ in range(Board.const_size())]

    @staticmethod
    def __assert_board(cells: Sequence[MutableSequence[Optional[Mark]]], expected: int) \
            -> None:
        assert len(cells) == expected, f"{len(cells)}, {expected}"
        for row in cells:
            assert len(row) == expected, f"{len(row)}, {expected}"

    def __repr__(self) -> str:
        return (f"{type(self).__qualname__}("
                f"cells={self.cells})")


@eq
class State:
    """Full game state which is enough to restore a saved game."""

    def __init__(
            self,
            game_rounds: int,
            players: Sequence[Player],
            board: Board,
            phase: Phase = Phase.BEGINNING,
            round_: int = 0,
            step: int = 0,
            required_ready: Optional[set[PlayerID]] = None):
        self.game_rounds: int = game_rounds
        assert len(players) == State.const_player_count(), \
            f"{len(players)}, {State.const_player_count()}"
        for (idx, player) in enumerate(players):
            assert player.id.idx == idx, f"{player.id.idx}, {idx}"
        self.players: Sequence[Player] = players
        self.board: Board = board
        self.phase: Phase = phase
        self.round: int = round_
        self.step: int = step
        self.required_ready: set[PlayerID] \
            = set(player.id for player in players) if required_ready is None \
            else required_ready

    def turn(self) -> PlayerID:
        """Returns `turn` - the `id` of the current `Player` in the `State.players`.

        `turn` is calculated in such a way as to alternate players order in different rounds.
        """
        return PlayerID((self.step + self.round) % len(self.players))

    @staticmethod
    def const_player_count() -> int:
        return 2

    def __repr__(self) -> str:
        return (f"{type(self).__qualname__}("
                f"game_rounds={self.game_rounds},"
                f"players={self.players},"
                f"board={self.board},"
                f"phase={self.phase},"
                f"round={self.round},"
                f"step={self.step},"
                f"required_ready={self.required_ready})")


class Action:
    def __init__(self, surrender: bool, occupy: Optional[Cell], ready: bool):
        assert ((surrender is True and occupy is None and ready is False)
                or (surrender is False and occupy is not None and ready is False)
                or (surrender is False and occupy is None and ready is True)), \
            "surrender={surrender}, occupy={occupy}, ready={ready}"
        self.__surrender: bool = surrender
        self.__occupy: Optional[Cell] = occupy
        self.__ready: bool = ready

    @staticmethod
    def new_surrender() -> Action:
        return Action(True, None, False)

    @staticmethod
    def new_occupy(cell: Cell) -> Action:
        return Action(False, cell, False)

    @staticmethod
    def new_ready() -> Action:
        return Action(False, None, True)

    @property
    def surrender(self) -> bool:
        return self.__surrender

    @property
    def occupy(self) -> Optional[Cell]:
        return self.__occupy

    @property
    def ready(self) -> bool:
        return self.__ready

    def __repr__(self) -> str:
        if self.__surrender is True:
            action = "surrender"
        elif self.__occupy is not None:
            action = f"occupy={self.__occupy}"
        elif self.__ready is True:
            action = "ready"
        else:
            assert False
        return (f"{type(self).__qualname__}("
                f"{action})")


class ActionQueue(ABC):
    @abstractmethod
    def player_id(self) -> PlayerID:
        pass

    @abstractmethod
    def pop(self) -> Optional[Action]:
        pass


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


class Logic:
    """Game logic."""

    def __init__(self, action_queues: Sequence[ActionQueue]):
        """Indexes in `action_queues` correspond to indexes in `State.players`."""
        assert len(action_queues) == State.const_player_count(), \
            f"{len(action_queues)}, {State.const_player_count()}"
        for (idx, action_queue) in enumerate(action_queues):
            assert action_queue.player_id().idx == idx, f"{action_queue.player_id().idx}, {idx}"
        self.__action_queues: Sequence[ActionQueue] = action_queues

    def advance(self, state: State) -> None:
        if Logic.is_game_over(state):
            return
        if state.phase is Phase.BEGINNING \
                or state.phase is Phase.OUTROUND:
            self.__advance_beginning_outround(state)
        elif state.phase is Phase.INROUND:
            self.__advance_inround(state)
        else:
            assert False

    def __advance_beginning_outround(self, state: State) -> None:
        for player_id in state.required_ready.copy():
            action = self.__action_queues[player_id.idx].pop()
            if action is None:
                pass
            elif action.ready is True:
                Logic.__ready(state, player_id)
            else:
                assert False

    def __advance_inround(self, state: State) -> None:
        player_id = state.turn()
        while True:
            action = self.__action_queues[player_id.idx].pop()
            if action is None:
                break
            elif action.surrender is True:
                Logic.__surrender(state)
            elif action.occupy is not None:
                Logic.__occupy(state, action.occupy)
            else:
                assert False
            if player_id != state.turn() or state.phase is not Phase.INROUND:
                break

    @staticmethod
    def __occupy(state: State, cell: Cell) -> None:
        assert state.phase is Phase.INROUND
        state.board.set(cell, state.players[state.turn().idx].mark)
        if Logic.is_win(state.board, cell):
            Logic.__win(state)
        elif Logic.__last_step(state.step, state.board):
            Logic.__draw(state)
        else:
            state.step += 1

    @staticmethod
    def is_win(board: Board, last_occupied: Cell) -> bool:
        h_match = 0
        v_match = 0
        d1_match = 0
        d2_match = 0
        x = last_occupied.x
        y = last_occupied.y
        mark = board.get(last_occupied)
        assert mark is not None
        for i in range(board.size()):
            if board.get(Cell(i, y)) == mark:
                h_match += 1
            if board.get(Cell(x, i)) == mark:
                v_match += 1
            if board.get((Cell(i, i))) == mark:
                d1_match += 1
            if board.get(Cell(i, board.size() - 1 - i)) == mark:
                d2_match += 1
        return (h_match == board.size() or v_match == board.size()
                or d1_match == board.size() or d2_match == board.size())

    @staticmethod
    def __last_step(step: int, board: Board) -> bool:
        return step == board.size() ** 2 - 1

    @staticmethod
    def __surrender(state: State) -> None:
        assert state.phase is Phase.INROUND
        # for more players this method would have been implemented quite differently
        assert State.const_player_count() == 2
        idx_other_player = (state.turn().idx + 1) % len(state.players)
        state.players[idx_other_player].wins += 1
        Logic.__end_round(state)

    @staticmethod
    def __win(state: State) -> None:
        state.players[state.turn().idx].wins += 1
        Logic.__end_round(state)

    @staticmethod
    def __draw(state: State) -> None:
        Logic.__end_round(state)

    @staticmethod
    def __ready(state: State, player_id: PlayerID) -> None:
        assert state.phase is Phase.BEGINNING or state.phase is Phase.OUTROUND
        state.required_ready.remove(player_id)
        if len(state.required_ready) == 0:
            if state.phase is Phase.OUTROUND:
                state.step = 0
                state.round += 1
                state.board.clear()
            elif state.phase is Phase.BEGINNING:
                pass
            else:
                assert False
            state.phase = Phase.INROUND

    @staticmethod
    def __end_round(state: State) -> None:
        state.phase = Phase.OUTROUND
        if not Logic.is_game_over(state):
            state.required_ready.update(set(player.id for player in state.players))

    @staticmethod
    def is_game_over(state: State) -> bool:
        return state.round == state.game_rounds - 1 and state.phase is Phase.OUTROUND

    def __repr__(self) -> str:
        return (f"{type(self).__qualname__}("
                f"action_queues={self.__action_queues})")


class AI(ABC):
    def act(self, state: State) -> None:
        pass


class World:
    def __init__(self, state: State, logic: Logic, ais: Sequence[AI]):
        self.__state: State = state
        self.__logic: Logic = logic
        self.__ais: Sequence[AI] = ais

    def advance(self) -> None:
        for ai in self.__ais:
            ai.act(self.__state)
        self.__logic.advance(self.__state)

    def __repr__(self) -> str:
        return (f"{type(self).__qualname__}("
                f"state={self.__state},"
                f"logic={self.__logic})")
