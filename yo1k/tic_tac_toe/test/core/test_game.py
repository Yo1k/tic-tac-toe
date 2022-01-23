from yo1k.tic_tac_toe.core.game import (
    ActionQueue,
    Action,
    Phase,
    Player,
    State,
    Logic,
    Board,
    Cell,
    Mark)
from collections.abc import Sequence
from typing import Optional
import unittest


class ListActionQueue(ActionQueue):
    def __init__(self, actions: Sequence[Optional[Action]]):
        self.actions = actions
        self.i = 0

    def next(self) -> Optional[Action]:
        if self.i >= len(self.actions):
            return None
        action = self.actions[self.i]
        self.i += 1
        return action


def _new_state(
        board: Optional[Board] = None,
        step: int = 0,
        round_: int = 0,
        phase: Phase = Phase.INROUND,
        player_x: Optional[Player] = None,
        player_o: Optional[Player] = None,
        game_rounds: int = 5,
        required_ready: Optional[set[int]] = None) -> State:
    player_x = Player(Mark.X) if player_x is None else player_x
    player_o = Player(Mark.O) if player_o is None else player_o
    board = Board() if board is None else board
    required_ready = set() if required_ready is None else required_ready
    return State(
            game_rounds=game_rounds, players=[player_x, player_o], board=board, phase=phase,
            round_=round_, step=step,required_ready=required_ready)


def _new_player(mark: Mark, wins: int) -> Player:
    player = Player(mark)
    player.wins = wins
    return player


class LogicSingleActionTest(unittest.TestCase):
    def test_advance__none_action(self):
        state = _new_state(board=Board([
                [None, None, None], [None, None, Mark.X], [None, None, None]]))
        Logic([ListActionQueue([None]), ListActionQueue([None])]).advance(state)
        expected_state = _new_state(
                board=Board([[None, None, None], [None, None, Mark.X], [None, None, None]]))
        self.assertEqual(expected_state, state)

    def test_advance__occupy_valid_action(self):
        state = _new_state()
        Logic([
                ListActionQueue([Action.new_occupy(Cell(1, 2))]),
                ListActionQueue([None])]) \
            .advance(state)
        expected_state = _new_state(
                board=Board([[None, None, None], [None, None, Mark.X], [None, None, None]]),
                step=1)
        self.assertEqual(expected_state, state)

    def test_advance__surrender_action(self):
        state = _new_state()
        Logic([
                ListActionQueue([Action.new_surrender()]),
                ListActionQueue([None])]) \
            .advance(state)
        expected_state = _new_state(
                board=Board([[None, None, None], [None, None, None], [None, None, None]]),
                phase=Phase.OUTROUND,
                player_o=_new_player(mark=Mark.O, wins=1),
                required_ready=set(range(2)))
        self.assertEqual(expected_state, state)

    def test_win_condition(self):
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
                actual = Logic._win_condition(Board(cells), cell)
                self.assertEqual(actual, expect)

    def test_advance__win(self):
        state = _new_state(
                board=Board([
                        [Mark.X, None, None], [Mark.O, Mark.X, Mark.O], [None, None, None]]),
                step=4)
        Logic([
                ListActionQueue([Action.new_occupy(Cell(2, 2))]),
                ListActionQueue([None])]) \
            .advance(state)
        expected_state = _new_state(
                board=Board([[Mark.X, None, None], [Mark.O, Mark.X, Mark.O], [None, None, Mark.X]]),
                step=4,
                phase=Phase.OUTROUND,
                player_x=_new_player(mark=Mark.X, wins=1),
                required_ready=set(range(2)))
        self.assertEqual(expected_state, state)

    def test_advance__draw(self):
        state = _new_state(
                board=Board([
                        [Mark.O, Mark.X, Mark.O],
                        [Mark.O, Mark.X, Mark.X],
                        [Mark.X, Mark.O, None]]),
                step=8)
        Logic([
                ListActionQueue([Action.new_occupy(Cell(2, 2))]),
                ListActionQueue([None])]) \
            .advance(state)
        expected_board_cells = [
                [Mark.O, Mark.X, Mark.O],
                [Mark.O, Mark.X, Mark.X],
                [Mark.X, Mark.O, Mark.X]]
        expected_state = _new_state(
                board=Board(expected_board_cells),
                step=8,
                phase=Phase.OUTROUND,
                required_ready=set(range(2)))
        self.assertEqual(expected_state, state)

    def test_advance__ready_action__outround(self):
        state = _new_state(
                board=Board([
                        [Mark.X, Mark.O, Mark.X],
                        [None, Mark.X, Mark.O],
                        [Mark.X, None, Mark.O]]),
                step=6,
                phase=Phase.OUTROUND,
                player_x=_new_player(Mark.X, 1),
                required_ready=set(range(1)))
        Logic([
                ListActionQueue([Action.new_ready()]),
                ListActionQueue([None])]) \
            .advance(state)
        expected_state = _new_state(
                board=Board([[None, None, None], [None, None, None], [None, None, None]]),
                step=0,
                round_=1,
                phase=Phase.INROUND,
                player_x=_new_player(Mark.X, 1))
        self.assertEqual(expected_state, state)

    def test_advance__ready_action__onset(self):
        state = _new_state(phase=Phase.BEGINNING, required_ready=set(range(1)))
        Logic([
                ListActionQueue([Action.new_ready()]),
                ListActionQueue([None])]) \
            .advance(state)
        expected_state = _new_state(
                board=Board([[None, None, None], [None, None, None], [None, None, None]]),
                step=0,
                round_=0,
                phase=Phase.INROUND)
        self.assertEqual(expected_state, state)


class LogicMultipleActionsTest(unittest.TestCase):
    def test_win(self):
        state = _new_state(phase=Phase.BEGINNING, required_ready=set(range(2)))
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
        logic = Logic([act_queue_px, act_queue_po])
        for i in range(0, len(act_queue_px.actions) + len(act_queue_po.actions)):
            logic.advance(state)
        expected_board_cells = [
                [Mark.X, Mark.O, Mark.X],
                [None, Mark.X, Mark.O],
                [Mark.X, None, Mark.O]]
        expected_state = _new_state(
                board=Board(expected_board_cells),
                step=6,
                round_=0,
                phase=Phase.OUTROUND,
                player_x=_new_player(mark=Mark.X, wins=1),
                required_ready=set(range(2)))
        self.assertEqual(expected_state, state)

    def test_draw(self):
        state = _new_state(round_=1, phase=Phase.INROUND)
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
        logic = Logic([act_queue_px, act_queue_po])
        for i in range(0, len(act_queue_px.actions) + len(act_queue_po.actions)):
            logic.advance(state)
        expected_board_cells = [
                [Mark.X, Mark.O, Mark.X],
                [Mark.X, Mark.O, Mark.O],
                [Mark.O, Mark.X, Mark.O]]
        expected_state = _new_state(
                board=Board(expected_board_cells),
                step=8,
                round_=1,
                phase=Phase.OUTROUND,
                required_ready=set(range(2)))
        self.assertEqual(expected_state, state)


if __name__ == "__main__":
    unittest.main()
