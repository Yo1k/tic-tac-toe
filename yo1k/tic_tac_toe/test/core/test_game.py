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
        game_rounds=5,
        player1=None,
        player2=None,
        board=None,
        phase=Phase.INROUND,
        round_=0,
        step=0) -> State:
    player1 = Player(Mark.X) if player1 is None else player1
    player2 = Player(Mark.O) if player2 is None else player2
    board = Board() if board is None else board
    return State(
            game_rounds=game_rounds, players=[player1, player2], board=board, phase=phase,
            round_=round_, step=step)


def _new_player(mark: Mark, wins: int) -> Player:
    player = Player(mark)
    player.wins = wins
    return player


class LogicSingleActionTest(unittest.TestCase):
    def test_advance__none_action(self):
        state = _new_state(board=Board([
                [None, None, None], [None, None, Mark.X], [None, None, None]]))
        Logic([ListActionQueue([None]), ListActionQueue([None])]).advance(state)
        expected_board_cells = [
                [None, None, None], [None, None, Mark.X], [None, None, None]]
        self.assertEqual(state.board.cells, expected_board_cells)
        self.assertEqual(state.step, 0)
        self.assertEqual(state.round, 0)
        self.assertEqual(state.phase, Phase.INROUND)
        self.assertEqual(state.players[0].wins, 0)
        self.assertEqual(state.players[1].wins, 0)

    def test_advance__occupy_valid_action(self):
        state = _new_state()
        Logic([
                ListActionQueue([Action.new_occupy(Cell(1, 2))]),
                ListActionQueue([None])]).advance(state)
        expected_board_cell = [
                [None, None, None], [None, None, Mark.X], [None, None, None]]
        self.assertEqual(state.board.cells, expected_board_cell)
        self.assertEqual(state.step, 1)
        self.assertEqual(state.round, 0)
        self.assertEqual(state.phase, Phase.INROUND)
        self.assertEqual(state.players[0].wins, 0)
        self.assertEqual(state.players[1].wins, 0)

    def test_advance__occupy_invalid_action(self):
        state = _new_state(board=Board([
                [None, None, None], [None, None, Mark.X], [None, None, None]]))
        Logic([
                ListActionQueue([Action.new_occupy(Cell(1, 2))]),
                ListActionQueue([None])]).advance(state)
        expected_board_cell = [
                [None, None, None], [None, None, Mark.X], [None, None, None]]
        self.assertEqual(state.board.cells, expected_board_cell)
        self.assertEqual(state.step, 1)
        self.assertEqual(state.round, 0)
        self.assertEqual(state.phase, Phase.INROUND)
        self.assertEqual(state.players[0].wins, 0)
        self.assertEqual(state.players[1].wins, 0)

    def test_advance__surrender_action(self):
        state = _new_state()
        Logic([
                ListActionQueue([Action.new_surrender()]),
                ListActionQueue([None])]).advance(state)
        expected_board_cells = [
                [None, None, None], [None, None, None], [None, None, None]]
        self.assertEqual(state.board.cells, expected_board_cells)
        self.assertEqual(state.step, 0)
        self.assertEqual(state.round, 0)
        self.assertEqual(state.phase, Phase.OUTROUND)
        self.assertEqual(state.players[0].wins, 0)
        self.assertEqual(state.players[1].wins, 1)

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
        for args_and_expect in args_and_expect_list:
            cells, cell, expect = args_and_expect
            actual = Logic.win_condition(Board(cells), cell)
            with self.subTest(expect=expect, cells=cells):
                self.assertEqual(actual, expect)

    def test_advance__win(self):
        state = _new_state(
                board=Board([
                        [Mark.X, None, None], [Mark.O, Mark.X, Mark.O], [None, None, None]]),
                step=4)
        Logic([
                ListActionQueue([Action.new_occupy(Cell(2, 2))]),
                ListActionQueue([None])]).advance(state)
        expected_board_cells = [
                [Mark.X, None, None], [Mark.O, Mark.X, Mark.O], [None, None, Mark.X]]
        self.assertEqual(state.board.cells, expected_board_cells)
        self.assertEqual(state.step, 4)
        self.assertEqual(state.round, 0)
        self.assertEqual(state.phase, Phase.OUTROUND)
        self.assertEqual(state.players[0].wins, 1)
        self.assertEqual(state.players[1].wins, 0)

    def test_advance__draw(self):
        state = _new_state(
                board=Board([
                        [Mark.O, Mark.X, Mark.O],
                        [Mark.O, Mark.X, Mark.X],
                        [Mark.X, Mark.O, None]]),
                step=8)
        Logic([
                ListActionQueue([Action.new_occupy(Cell(2, 2))]),
                ListActionQueue([None])]).advance(state)
        expected_board_cells = [
                [Mark.O, Mark.X, Mark.O],
                [Mark.O, Mark.X, Mark.X],
                [Mark.X, Mark.O, Mark.X]]
        self.assertEqual(state.board.cells, expected_board_cells)
        self.assertEqual(state.step, 8)
        self.assertEqual(state.round, 0)
        self.assertEqual(state.phase, Phase.OUTROUND)
        self.assertEqual(state.players[0].wins, 0)
        self.assertEqual(state.players[1].wins, 0)

    def test_advance__start_action__outround(self):
        state = _new_state(
                player1=_new_player(Mark.X, 1),
                board=Board([
                        [Mark.X, Mark.O, Mark.X],
                        [None, Mark.X, Mark.O],
                        [Mark.X, None, Mark.O]]),
                phase=Phase.OUTROUND, step=6)
        Logic([
                ListActionQueue([Action.new_start()]),
                ListActionQueue([None])]).advance(state)
        expected_board_cells = [[None, None, None], [None, None, None], [None, None, None]]
        self.assertEqual(state.board.cells, expected_board_cells)
        self.assertEqual(state.step, 0)
        self.assertEqual(state.round, 1)
        self.assertEqual(state.phase, Phase.INROUND)
        self.assertEqual(state.players[0].wins, 1)
        self.assertEqual(state.players[1].wins, 0)

    def test_advance__start_action__onset(self):
        state = _new_state(phase=Phase.BEGINNING)
        Logic([
                ListActionQueue([Action.new_start()]),
                ListActionQueue([None])]).advance(state)
        expected_board_cells = [[None, None, None], [None, None, None], [None, None, None]]
        self.assertEqual(state.board.cells, expected_board_cells)
        self.assertEqual(state.step, 0)
        self.assertEqual(state.round, 0)
        self.assertEqual(state.phase, Phase.INROUND)
        self.assertEqual(state.players[0].wins, 0)
        self.assertEqual(state.players[1].wins, 0)


class LogicMultipleActionsTest(unittest.TestCase):
    def test_win(self):
        state = _new_state(phase=Phase.BEGINNING)
        act_queue_px = ListActionQueue([
                Action.new_start(),
                Action.new_occupy(Cell(1, 1)),
                None,
                Action.new_occupy(Cell(0, 0)),
                Action.new_occupy(Cell(0, 2)),
                Action.new_occupy(Cell(2, 0))])
        act_queue_po = ListActionQueue([
                Action.new_occupy(Cell(1, 2)),
                Action.new_occupy(Cell(2, 2)),
                None,
                Action.new_occupy(Cell(0, 1))])
        expected_board_cells = [
                [Mark.X, Mark.O, Mark.X],
                [None, Mark.X, Mark.O],
                [Mark.X, None, Mark.O]]
        for i in range(0, len(act_queue_px.actions) + len(act_queue_po.actions)):
            Logic([act_queue_px, act_queue_po]).advance(state)
        self.assertEqual(state.board.cells, expected_board_cells)
        self.assertEqual(state.step, 6)
        self.assertEqual(state.round, 0)
        self.assertEqual(state.phase, Phase.OUTROUND)
        self.assertEqual(state.players[0].wins, 1)
        self.assertEqual(state.players[1].wins, 0)

    def test_draw(self):
        state = _new_state(phase=Phase.INROUND, round_=1)
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
        expected_board_cells = [
                [Mark.X, Mark.O, Mark.X],
                [Mark.X, Mark.O, Mark.O],
                [Mark.O, Mark.X, Mark.O]]
        for i in range(0, len(act_queue_px.actions) + len(act_queue_po.actions)):
            Logic([act_queue_px, act_queue_po]).advance(state)
        self.assertEqual(state.board.cells, expected_board_cells)
        self.assertEqual(state.step, 8)
        self.assertEqual(state.round, 1)
        self.assertEqual(state.phase, Phase.OUTROUND)
        self.assertEqual(state.players[0].wins, 0)
        self.assertEqual(state.players[1].wins, 0)


if __name__ == "__main__":
    unittest.main()
