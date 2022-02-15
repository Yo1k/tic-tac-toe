import unittest
from collections.abc import MutableSequence, Sequence
from typing import Optional
from yo1k.tic_tac_toe.kernel.game import (
    ActionQueue,
    Action,
    Phase,
    Player,
    State,
    Logic,
    Board,
    Cell,
    Mark)


class ListActionQueue(ActionQueue):
    def __init__(self, actions: MutableSequence[Optional[Action]]):
        self.actions: MutableSequence[Optional[Action]] = actions
        self.actions.reverse()

    def pop(self) -> Optional[Action]:
        if len(self.actions) == 0:
            return None
        else:
            return self.actions.pop()


def _new_state(
        game_rounds: int = 5,
        player_x: Optional[Player] = None,
        player_o: Optional[Player] = None,
        board: Optional[Board] = None,
        phase: Phase = Phase.INROUND,
        round_: int = 0,
        step: int = 0,
        required_ready: Optional[set[int]] = None) -> State:
    player_x = Player(Mark.X) if player_x is None else player_x
    player_o = Player(Mark.O) if player_o is None else player_o
    board = Board() if board is None else board
    required_ready = set() if required_ready is None else required_ready
    return State(
            game_rounds=game_rounds, players=(player_x, player_o), board=board, phase=phase,
            round_=round_, step=step, required_ready=required_ready)


def _new_player(mark: Mark, wins: int) -> Player:
    player = Player(mark)
    player.wins = wins
    return player


class LogicSingleActionTest(unittest.TestCase):
    def test_advance__no_action(self) -> None:
        state = _new_state(board=Board([
                [None, None, None], [None, None, Mark.X], [None, None, None]]))
        Logic((ListActionQueue([]), ListActionQueue([]))).advance(state)
        expected_state = _new_state(
                board=Board([[None, None, None], [None, None, Mark.X], [None, None, None]]))
        self.assertEqual(expected_state, state)

    def test_advance__occupy_action(self) -> None:
        state = _new_state()
        Logic((
                ListActionQueue([Action.new_occupy(Cell(1, 2))]),
                ListActionQueue([]))) \
            .advance(state)
        expected_state = _new_state(
                board=Board([[None, None, None], [None, None, Mark.X], [None, None, None]]),
                step=1)
        self.assertEqual(expected_state, state)

    def test_advance__surrender_action(self) -> None:
        state = _new_state()
        expected_required_ready = set(range(len(state.players)))
        Logic((
                ListActionQueue([Action.new_surrender()]),
                ListActionQueue([]))) \
            .advance(state)
        expected_state = _new_state(
                player_o=_new_player(mark=Mark.O, wins=1),
                board=Board([[None, None, None], [None, None, None], [None, None, None]]),
                phase=Phase.OUTROUND,
                required_ready=expected_required_ready)
        self.assertEqual(expected_state, state)

    def test_win_condition(self) -> None:
        args_and_expect_list = [
                ([[Mark.X, Mark.X, Mark.X], [None, None, None], [None, None, None]],
                 Cell(0, 0), True),
                ([[None, None, None], [Mark.X, Mark.X, Mark.X], [None, None, None]],
                 Cell(1, 0), True),
                ([[None, None, None], [None, None, None], [Mark.X, Mark.X, Mark.X]],
                 Cell(2, 0), True),
                ([[Mark.X, None, None], [Mark.X, None, None], [Mark.X, None, None]],
                 Cell(1, 0), True),
                ([[None, Mark.X, None], [None, Mark.X, None], [None, Mark.X, None]],
                 Cell(1, 1), True),
                ([[None, None, Mark.X], [None, None, Mark.X], [None, None, Mark.X]],
                 Cell(1, 2), True),
                ([[Mark.X, None, None], [None, Mark.X, None], [None, None, Mark.X]],
                 Cell(1, 1), True),
                ([[None, None, Mark.X], [None, Mark.X, None], [Mark.X, None, None]],
                 Cell(1, 1), True),
                ([[Mark.X, Mark.X, None], [Mark.X, None, None], [None, None, None]],
                 Cell(1, 0), False),
                ([[Mark.X, None, None], [None, None, Mark.X], [None, Mark.X, None]],
                 Cell(0, 0), False),
                ([[None, Mark.X, None], [None, None, Mark.X], [None, Mark.X, None]],
                 Cell(0, 1), False),
                ([[Mark.X, Mark.O, Mark.X], [None, None, None], [None, None, None]],
                 Cell(0, 2), False)]
        for cells, cell, expect in args_and_expect_list:
            with self.subTest(expect=expect, cell=cell, cells=cells):
                actual = Logic.win_condition(Board(cells), cell)  # type: ignore
                self.assertEqual(actual, expect)

    def test_advance__win(self) -> None:
        state = _new_state(
                board=Board([
                        [Mark.X, None, None], [Mark.O, Mark.X, Mark.O], [None, None, None]]),
                step=4)
        expected_required_ready = set(range(len(state.players)))
        Logic((
                ListActionQueue([Action.new_occupy(Cell(2, 2))]),
                ListActionQueue([]))) \
            .advance(state)
        expected_state = _new_state(
                player_x=_new_player(mark=Mark.X, wins=1),
                board=Board([[Mark.X, None, None], [Mark.O, Mark.X, Mark.O], [None, None, Mark.X]]),
                step=4,
                phase=Phase.OUTROUND,
                required_ready=expected_required_ready)
        self.assertEqual(expected_state, state)

    def test_advance__draw(self) -> None:
        state = _new_state(
                board=Board([
                        [Mark.O, Mark.X, Mark.O],
                        [Mark.O, Mark.X, Mark.X],
                        [Mark.X, Mark.O, None]]),
                step=8)
        expected_required_ready = set(range(len(state.players)))
        Logic((
                ListActionQueue([Action.new_occupy(Cell(2, 2))]),
                ListActionQueue([]))) \
            .advance(state)
        expected_board_cells: Sequence[MutableSequence[Optional[Mark]]] = [
                [Mark.O, Mark.X, Mark.O],
                [Mark.O, Mark.X, Mark.X],
                [Mark.X, Mark.O, Mark.X]]
        expected_state = _new_state(
                board=Board(expected_board_cells),
                phase=Phase.OUTROUND,
                step=8,
                required_ready=expected_required_ready)
        self.assertEqual(expected_state, state)

    def test_advance__ready_action__outround(self) -> None:
        state = _new_state(
                player_x=_new_player(mark=Mark.X, wins=1),
                board=Board([
                        [Mark.X, Mark.O, Mark.X],
                        [None, Mark.X, Mark.O],
                        [Mark.X, None, Mark.O]]),
                phase=Phase.OUTROUND,
                step=6,
                required_ready={0})
        Logic((
                ListActionQueue([Action.new_ready()]),
                ListActionQueue([]))) \
            .advance(state)
        expected_state = _new_state(
                player_x=_new_player(mark=Mark.X, wins=1),
                board=Board([[None, None, None], [None, None, None], [None, None, None]]),
                phase=Phase.INROUND,
                round_=1,
                step=0)
        self.assertEqual(expected_state, state)

    def test_advance__ready_action__beginning(self) -> None:
        state = _new_state(phase=Phase.BEGINNING, required_ready={0})
        Logic((
                ListActionQueue([Action.new_ready()]),
                ListActionQueue([]))) \
            .advance(state)
        expected_state = _new_state(
                board=Board([[None, None, None], [None, None, None], [None, None, None]]),
                phase=Phase.INROUND,
                round_=0,
                step=0)
        self.assertEqual(expected_state, state)

    def test_advance__stop_at__phase_change(self) -> None:
        state = _new_state()
        expected_required_ready = set(range(len(state.players)))
        Logic((
                ListActionQueue([Action.new_surrender(), Action.new_occupy(Cell(0, 0))]),
                ListActionQueue([]))) \
            .advance(state)
        expected_state = _new_state(
                player_o=_new_player(mark=Mark.O, wins=1),
                board=Board([[None, None, None], [None, None, None], [None, None, None]]),
                phase=Phase.OUTROUND,
                required_ready=expected_required_ready)
        self.assertEqual(expected_state, state)


class LogicMultipleActionsTest(unittest.TestCase):
    def test_win(self) -> None:
        state = _new_state(
                phase=Phase.BEGINNING,
                required_ready=set(range(State.const_player_count())))
        expected_required_ready = set(range(len(state.players)))
        act_queue_px = ListActionQueue([
                None,
                None,
                Action.new_ready(),
                Action.new_occupy(Cell(1, 1)),
                None,
                Action.new_occupy(Cell(0, 0)),
                Action.new_occupy(Cell(0, 2)),
                Action.new_occupy(Cell(2, 0))])
        act_queue_po = ListActionQueue([
                Action.new_ready(),
                Action.new_occupy(Cell(1, 2)),
                Action.new_occupy(Cell(2, 2)),
                None,
                Action.new_occupy(Cell(0, 1))])
        logic = Logic((act_queue_px, act_queue_po))
        while len(act_queue_px.actions) + len(act_queue_po.actions) > 0:
            logic.advance(state)
        expected_board_cells: Sequence[MutableSequence[Optional[Mark]]] = [
                [Mark.X, Mark.O, Mark.X],
                [None, Mark.X, Mark.O],
                [Mark.X, None, Mark.O]]
        expected_state = _new_state(
                player_x=_new_player(mark=Mark.X, wins=1),
                board=Board(expected_board_cells),
                phase=Phase.OUTROUND,
                round_=0,
                step=6,
                required_ready=expected_required_ready)
        self.assertEqual(expected_state, state)

    def test_draw(self) -> None:
        state = _new_state(phase=Phase.INROUND, round_=1)
        expected_required_ready = set(range(len(state.players)))
        act_queue_px = ListActionQueue([
                Action.new_occupy(Cell(0, 0)),
                Action.new_occupy(Cell(1, 0)),
                Action.new_occupy(Cell(0, 2)),
                Action.new_occupy(Cell(2, 1))])
        act_queue_po = ListActionQueue([
                Action.new_occupy(Cell(1, 1)),
                Action.new_occupy(Cell(1, 2)),
                Action.new_occupy(Cell(2, 0)),
                Action.new_occupy(Cell(0, 1)),
                Action.new_occupy(Cell(2, 2))])
        logic = Logic((act_queue_px, act_queue_po))
        while len(act_queue_px.actions) + len(act_queue_po.actions) > 0:
            logic.advance(state)
        expected_board_cells: Sequence[MutableSequence[Optional[Mark]]] = [
                [Mark.X, Mark.O, Mark.X],
                [Mark.X, Mark.O, Mark.O],
                [Mark.O, Mark.X, Mark.O]]
        expected_state = _new_state(
                board=Board(expected_board_cells),
                phase=Phase.OUTROUND,
                round_=1,
                step=8,
                required_ready=expected_required_ready)
        self.assertEqual(expected_state, state)


if __name__ == "__main__":
    unittest.main()
