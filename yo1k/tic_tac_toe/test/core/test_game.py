import yo1k.tic_tac_toe.core.game as g
from collections.abc import Sequence
from typing import Optional
import unittest


class ListActionQueue(g.ActionQueue):
    def __init__(self, actions: Sequence[Optional[g.Action]]):
        self.actions = actions
        self.i = 0

    def next(self) -> Optional[g.Action]:
        if self.i > len(self.actions):
            return None
        action = self.actions[self.i]
        self.i += 1
        return action


class StateSetup:
    @staticmethod
    def _set_state(
            game_rounds=5,
            player1=None,
            player2=None,
            board=None,
            phase=g.Phase.INROUND,
            cur_round=0,
            step=0) -> g.State:
        player1 = g.Player(g.Mark.X) if player1 is None else player1
        player2 = g.Player(g.Mark.O) if player2 is None else player2
        board = g.Board() if board is None else board
        return g.State(game_rounds, [player1, player2], board, phase, cur_round, step)

    @staticmethod
    def _set_player(mark: g.Mark, wins: int) -> g.Player:
        player = g.Player(mark)
        player.wins = wins
        return player


class LogicSingleActionTest(unittest.TestCase):
    def test_advance_none_action(self):
        previous_game_state_board = [
            [None, None, None], [None, None, g.Mark.X], [None, None, None]]
        game_state = StateSetup._set_state(board=g.Board(previous_game_state_board))
        g.Logic([ListActionQueue([None]), []]).advance(game_state)
        next_game_state_board = [
            [None, None, None], [None, None, g.Mark.X], [None, None, None]]
        self.assertEqual(game_state.board.cells, next_game_state_board)
        self.assertEqual(game_state.step, 0)
        self.assertEqual(game_state.round, 0)
        self.assertEqual(game_state.phase, g.Phase.INROUND)
        self.assertEqual(game_state.players[0].wins, 0)
        self.assertEqual(game_state.players[1].wins, 0)

    def test_advance_occupy_valid_action(self):
        game_state = StateSetup._set_state()
        act_queue_p1 = ListActionQueue([g.Action.new_occupy(g.Cell(1, 2))])
        g.Logic([act_queue_p1, []]).advance(game_state)
        next_game_state_board = [
            [None, None, None], [None, None, g.Mark.X], [None, None, None]]
        self.assertEqual(game_state.board.cells, next_game_state_board)
        self.assertEqual(game_state.step, 1)
        self.assertEqual(game_state.round, 0)
        self.assertEqual(game_state.phase, g.Phase.INROUND)
        self.assertEqual(game_state.players[0].wins, 0)
        self.assertEqual(game_state.players[1].wins, 0)

    def test_advance_occupy_invalid_action(self):
        previous_game_state_board = [
            [None, None, None], [None, None, g.Mark.X], [None, None, None]]
        game_state = StateSetup._set_state(board=g.Board(previous_game_state_board))
        act_queue_p1 = ListActionQueue([g.Action.new_occupy(g.Cell(1, 2))])
        g.Logic([act_queue_p1, []]).advance(game_state)
        next_game_state_board = [
            [None, None, None], [None, None, g.Mark.X], [None, None, None]]
        self.assertEqual(game_state.board.cells, next_game_state_board)
        self.assertEqual(game_state.step, 1)
        self.assertEqual(game_state.round, 0)
        self.assertEqual(game_state.phase, g.Phase.INROUND)
        self.assertEqual(game_state.players[0].wins, 0)
        self.assertEqual(game_state.players[1].wins, 0)

    def test_advance_surrender_action(self):
        game_state = StateSetup._set_state()
        act_queue_p1 = ListActionQueue([g.Action.new_surrender()])
        g.Logic([act_queue_p1, []]).advance(game_state)
        next_game_state_board = [
            [None, None, None], [None, None, None], [None, None, None]]
        self.assertEqual(game_state.board.cells, next_game_state_board)
        self.assertEqual(game_state.step, 0)
        self.assertEqual(game_state.round, 0)
        self.assertEqual(game_state.phase, g.Phase.OUTROUND)
        self.assertEqual(game_state.players[0].wins, 0)
        self.assertEqual(game_state.players[1].wins, 1)

    def test_win_condition(self):  # SKTODO rename lists and try to pack them
        list_of_cell_and_win_board = [
            (g.Cell(0, 0),
             [[g.Mark.X, g.Mark.X, g.Mark.X], [None, None, None], [None, None, None]]),
            (g.Cell(1, 0),
             [[None, None, None], [g.Mark.X, g.Mark.X, g.Mark.X], [None, None, None]]),
            (g.Cell(2, 0),
             [[None, None, None], [None, None, None], [g.Mark.X, g.Mark.X, g.Mark.X]]),
            (g.Cell(1, 0),
             [[g.Mark.X, None, None], [g.Mark.X, None, None], [g.Mark.X, None, None]]),
            (g.Cell(1, 1),
             [[None, g.Mark.X, None], [None, g.Mark.X, None], [None, g.Mark.X, None]]),
            (g.Cell(1, 2),
             [[None, None, g.Mark.X], [None, None, g.Mark.X], [None, None, g.Mark.X]]),
            (g.Cell(1, 1),
             [[g.Mark.X, None, None], [None, g.Mark.X, None], [None, None, g.Mark.X]]),
            (g.Cell(1, 1),
             [[None, None, g.Mark.X], [None, g.Mark.X, None], [g.Mark.X, None, None]])]
        for i in list_of_cell_and_win_board:
            cell, win_board = i
            game_state = StateSetup._set_state(board=g.Board(win_board))
            with self.subTest(win_board=game_state.board.cells):
                self.assertTrue(g.Logic._win_condition(game_state.board, cell))

    def test_not_win_condition(self):
        list_of_cell_and_not_win_board = [
            (g.Cell(1, 0),
             [[g.Mark.X, g.Mark.X, None], [g.Mark.X, None, None], [None, None, None]]),
            (g.Cell(0, 0),
             [[g.Mark.X, None, None], [None, None, g.Mark.X], [None, g.Mark.X, None]]),
            (g.Cell(0, 1),
             [[None, g.Mark.X, None], [None, None, g.Mark.X], [None, g.Mark.X, None]]),
            (g.Cell(0, 2),
             [[g.Mark.X, g.Mark.O, g.Mark.X], [None, None, None], [None, None, None]])]
        for i in list_of_cell_and_not_win_board:
            cell, not_win_board = i
            game_state = StateSetup._set_state(board=g.Board(not_win_board))
            with self.subTest(not_win_board=game_state.board.cells):
                self.assertFalse(g.Logic._win_condition(game_state.board, cell))

    def test_advance_win_action(self):
        previous_game_state_board = [
            [g.Mark.X, None, None], [g.Mark.O, g.Mark.X, g.Mark.O], [None, None, None]]
        game_state = StateSetup._set_state(
            board=g.Board(previous_game_state_board),
            step=4)
        act_queue_p1 = ListActionQueue([g.Action.new_occupy(g.Cell(2, 2))])
        g.Logic([act_queue_p1, []]).advance(game_state)
        next_game_state_board = [
            [g.Mark.X, None, None], [g.Mark.O, g.Mark.X, g.Mark.O], [None, None, g.Mark.X]]
        self.assertEqual(game_state.board.cells, next_game_state_board)
        self.assertEqual(game_state.step, 4)
        self.assertEqual(game_state.round, 0)
        self.assertEqual(game_state.phase, g.Phase.OUTROUND)
        self.assertEqual(game_state.players[0].wins, 1)
        self.assertEqual(game_state.players[1].wins, 0)

    def test_advance_draw_action(self):
        previous_game_state_board = [
            [g.Mark.O, g.Mark.X, g.Mark.O],
            [g.Mark.O, g.Mark.X, g.Mark.X],
            [g.Mark.X, g.Mark.O, None]]
        game_state = StateSetup._set_state(
            board=g.Board(previous_game_state_board),
            step=8)
        act_queue_p1 = ListActionQueue([g.Action.new_occupy(g.Cell(2, 2))])
        g.Logic([act_queue_p1, []]).advance(game_state)
        next_game_state_board = [
            [g.Mark.O, g.Mark.X, g.Mark.O],
            [g.Mark.O, g.Mark.X, g.Mark.X],
            [g.Mark.X, g.Mark.O, g.Mark.X]]
        self.assertEqual(game_state.board.cells, next_game_state_board)
        self.assertEqual(game_state.step, 8)
        self.assertEqual(game_state.round, 0)
        self.assertEqual(game_state.phase, g.Phase.OUTROUND)
        self.assertEqual(game_state.players[0].wins, 0)
        self.assertEqual(game_state.players[1].wins, 0)

    def test_advance_next_round_action_outround(self):
        previous_game_state_board = [
            [g.Mark.X, g.Mark.O, g.Mark.X],
            [None, g.Mark.X, g.Mark.O],
            [g.Mark.X, None, g.Mark.O]]
        game_state = StateSetup._set_state(
            player1=StateSetup._set_player(g.Mark.X, 1),
            board=g.Board(previous_game_state_board),
            phase=g.Phase.OUTROUND, step=6)
        act_queue_p1 = ListActionQueue([g.Action.new_start()])
        g.Logic([act_queue_p1, []]).advance(game_state)
        next_game_state_board = [[None, None, None], [None, None, None], [None, None, None]]
        self.assertEqual(game_state.board.cells, next_game_state_board)
        self.assertEqual(game_state.step, 0)
        self.assertEqual(game_state.round, 1)
        self.assertEqual(game_state.phase, g.Phase.INROUND)
        self.assertEqual(game_state.players[0].wins, 1)
        self.assertEqual(game_state.players[1].wins, 0)

    def test_advance_next_round_action_onset(self):
        game_state = StateSetup._set_state(phase=g.Phase.ONSET)
        act_queue_p1 = ListActionQueue([g.Action.new_start()])
        g.Logic([act_queue_p1, []]).advance(game_state)
        next_game_state_board = [[None, None, None], [None, None, None], [None, None, None]]
        self.assertEqual(game_state.board.cells, next_game_state_board)
        self.assertEqual(game_state.step, 0)
        self.assertEqual(game_state.round, 0)
        self.assertEqual(game_state.phase, g.Phase.INROUND)
        self.assertEqual(game_state.players[0].wins, 0)
        self.assertEqual(game_state.players[1].wins, 0)


class LogicQueueActionTest(unittest.TestCase):
    def test_win_cur_round_0(self):
        game_state = StateSetup._set_state(phase=g.Phase.ONSET)
        act_queue_p1 = ListActionQueue([
            g.Action.new_start(),
            g.Action.new_occupy(g.Cell(1, 1)),
            None,
            g.Action.new_occupy(g.Cell(0, 0)),
            g.Action.new_occupy(g.Cell(0, 2)),
            g.Action.new_occupy(g.Cell(2, 0))])
        act_queue_p2 = ListActionQueue([
            g.Action.new_occupy(g.Cell(1, 2)),
            g.Action.new_occupy(g.Cell(2, 2)),
            None,
            g.Action.new_occupy(g.Cell(0, 1))])
        finish_game_state_board = [
            [g.Mark.X, g.Mark.O, g.Mark.X],
            [None, g.Mark.X, g.Mark.O],
            [g.Mark.X, None, g.Mark.O]]
        while game_state.phase is not g.Phase.OUTROUND:
            g.Logic([act_queue_p1, act_queue_p2]).advance(game_state)
        self.assertEqual(game_state.board.cells, finish_game_state_board)
        self.assertEqual(game_state.step, 6)
        self.assertEqual(game_state.round, 0)
        self.assertEqual(game_state.phase, g.Phase.OUTROUND)
        self.assertEqual(game_state.players[0].wins, 1)
        self.assertEqual(game_state.players[1].wins, 0)

    def test_draw_cur_round_1(self):
        game_state = StateSetup._set_state(phase=g.Phase.INROUND, cur_round=1)
        act_queue_p1 = ListActionQueue([
            g.Action.new_occupy(g.Cell(0, 0)),
            g.Action.new_occupy(g.Cell(1, 0)),
            g.Action.new_occupy(g.Cell(0, 2)),
            g.Action.new_occupy(g.Cell(2, 1))])
        act_queue_p2 = ListActionQueue([
            g.Action.new_occupy(g.Cell(1, 1)),
            g.Action.new_occupy(g.Cell(1, 2)),
            g.Action.new_occupy(g.Cell(2, 0)),
            g.Action.new_occupy(g.Cell(0, 1)),
            g.Action.new_occupy(g.Cell(2, 2))])
        finish_game_state_board = [
            [g.Mark.X, g.Mark.O, g.Mark.X],
            [g.Mark.X, g.Mark.O, g.Mark.O],
            [g.Mark.O, g.Mark.X, g.Mark.O]]
        while game_state.phase is not g.Phase.OUTROUND:
            g.Logic([act_queue_p1, act_queue_p2]).advance(game_state)
        self.assertEqual(game_state.board.cells, finish_game_state_board)
        self.assertEqual(game_state.step, 8)
        self.assertEqual(game_state.round, 1)
        self.assertEqual(game_state.phase, g.Phase.OUTROUND)
        self.assertEqual(game_state.players[0].wins, 0)
        self.assertEqual(game_state.players[1].wins, 0)


if __name__ == "__main__":
    unittest.main()
