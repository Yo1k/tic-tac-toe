#!/usr/bin/env python3
import sys
from collections.abc import Sequence
from random import randrange
from typing import Optional

from asciimatics.event import KeyboardEvent, MouseEvent
from asciimatics.exceptions import ResizeScreenError
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, Button, Widget, Divider, VerticalDivider

from yo1k.tic_tac_toe.ai import RandomAI
from yo1k.tic_tac_toe.game import Mark, Cell, DefaultActionQueue, State, Action, World, PlayerID, \
    Board, Player, Phase, Logic


class GameInfoWidget(Widget):
    def __init__(self, state: State):
        super().__init__(
                name=f"{type(self).__qualname__}",
                tab_stop=False)
        self.__state: State = state

    def update(self, frame_no):
        (colour, attr, bg) = self._pick_colours("button")
        widget_text = f"round {self.__state.round + 1}/{self.__state.game_rounds}"
        self._frame.canvas.print_at(
                widget_text,
                self._x + self._offset
                + self.width // 2
                - len(widget_text) // 2,
                self._y,
                colour, attr, bg)

    def reset(self):
        pass

    def process_event(self, event):
        pass

    def required_height(self, offset, width):
        return 2

    @property
    def value(self):
        """
        The current value for this `GameInfoWidget`.
        """
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class PlayerWidget(Widget):
    def __init__(self, state: State, player_id: PlayerID):
        super().__init__(
                name=f"{type(self).__qualname__}",
                tab_stop=False)
        self.__state: State = state
        self.__player_id = player_id

    def update(self, frame_no):
        (colour, attr, bg) = self._pick_colours("button")
        widget_text = f"wins: {self.__state.players[self.__player_id.idx].wins}"
        self._frame.canvas.print_at(
                widget_text,
                self._x + self._offset
                + self.width // 2
                - len(widget_text) // 2,
                self._y,
                colour, attr, bg)

    def reset(self):
        pass

    def process_event(self, event):
        pass

    def required_height(self, offset, width):
        return 3

    @property
    def value(self):
        """
        The current value for this `GameInfoWidget`.
        """
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class CellWidget(Widget):
    def __init__(self, state: State, cell: Cell):
        super().__init__(
                name=f"{type(self).__qualname__}",
                tab_stop=False)
        self.__state: State = state
        self.__cell: Cell = cell

    def required_height(self, offset, width):
        return 3

    def update(self, frame_no):
        (colour, attr, bg) = self._pick_colours("button")
        self._frame.canvas.print_at(
            f"{self.__state.board.get(self.__cell)}",
            self._x + self._offset
            + self.width // 2
            - len(f"{self.__state.board.get(self.__cell)}") // 2,
            self._y,
            colour, attr, bg)

    def reset(self):
        pass

    def process_event(self, event):
        if isinstance(event, MouseEvent):
            if event.buttons != 0 and self.is_mouse_over(event, include_label=False):
                # self.__actions.add(Action.new_occupy(self.__cell))
                return None
        # Ignore other events
        return event

    @property
    def value(self):
        """
        The current value for this `CellWidget`.
        """
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class EventLoopEntryPoint(Widget):
    def __init__(self, world: World):
        super().__init__(name="EventLoopEntryPoint")
        self.__world = world

    def update(self, frame_no):
        self.__world.advance()

    def reset(self):
        self._value = False

    def process_event(self, event):
        pass

    def required_height(self, offset, width):
        return 1

    @property
    def value(self):
        """
        The current value for this Button.
        """
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    @property
    def frame_update_count(self):
        """
        The number of frames before this Widget should be updated.
        """
        return 20


class GameView(Frame):
    def __init__(
            self,
            screen: Screen,
            state: State,
            action_queues: Sequence[DefaultActionQueue],
            world: World,):
        super().__init__(
                screen,
                screen.height,
                screen.width,
                hover_focus=True,
                can_scroll=False,
                title=f"{type(self).__qualname__}",
                has_border=False)
        self.state = state
        self.action_queues = action_queues
        self.world = world

        # SKTODO Create board more readable
        self.cells = [[
                CellWidget(self.state, Cell(x, y))
                for x in range(self.state.board.size())]
                for y in range(self.state.board.size())]
        # self.cells = []
        # for x in range(self.state.board.size()):
        #     for y in range(self.state.board.size()):
        #         self.cells.append(CellButton(
        #                 Cell(x, y),
        #                 self.action_queue))

        layout_game_info = Layout([100], fill_frame=False)
        self.add_layout(layout_game_info)
        layout_game_info.add_widget(GameInfoWidget(self.state))
        layout_game_info.add_widget(Divider())

        layout = Layout([0.5, 0.1, 1, 1, 1, 0.1, 0.5], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(PlayerWidget(self.state, PlayerID(0)), 0)
        layout.add_widget(PlayerWidget(self.state, PlayerID(1)), 6)
        layout.add_widget(VerticalDivider(), 1)
        layout.add_widget(VerticalDivider(), 5)
        for x in range(2, 5):
            for y in range(2, 5):
                layout.add_widget(self.cells[x - 2][y - 2], x)

        layout2 = Layout([100])
        self.add_layout(layout2)
        advance_loop = EventLoopEntryPoint(self.world)
        layout2.add_widget(advance_loop)

        self.fix()


renderer = FigletText(text="X", width=10)


if __name__ == '__main__':
    ai_rng_seed_px = randrange(sys.maxsize)
    ai_rng_seed_po = randrange(sys.maxsize)
    player_x = Player(PlayerID(0), Mark.X)
    player_o = Player(PlayerID(1), Mark.O)
    act_queue_px = DefaultActionQueue(player_x.id)
    act_queue_po = DefaultActionQueue(player_o.id)
    g_state = State(
            game_rounds=20,
            board=Board(),
            players=(player_x, player_o))
    logic = Logic((act_queue_px, act_queue_po))
    g_world = World(
            g_state,
            logic,
            (
                    RandomAI(player_x.id, ai_rng_seed_px, act_queue_px),
                    RandomAI(player_o.id, ai_rng_seed_po, act_queue_po)
            ))

    last_scene = None


    def render_game_view(screen: Screen, scene: Scene):
        scenes = [Scene([GameView(screen, g_state, (act_queue_px, act_queue_po), g_world)], -1)]
        screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

    while True:

        try:
            Screen.wrapper(render_game_view, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
