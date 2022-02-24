#!/usr/bin/env python3
import sys
from asciimatics.event import KeyboardEvent, MouseEvent
from asciimatics.exceptions import ResizeScreenError
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, Button


class State:
    def __init__(self):
        self.mark = "    X    "


class CellButton(Button):
    def __init__(self, mark):
        super().__init__(text="None", on_click=None, add_box=False)
        self.mark = mark

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord(" "), 10, 13]:
                self.text = self.mark

                return None
            # Ignore any other key press.
            return event
        if isinstance(event, MouseEvent):
            if event.buttons != 0 and self.is_mouse_over(event, include_label=False):
                self.text = self.mark
                return None
        # Ignore other events
        return event

    def _on_click(self):
        self.text = self.mark


class GameView(Frame):
    def __init__(self, screen, state: State):
        super().__init__(
                screen,
                screen.height * 2 // 3,
                screen.width * 2 // 3,
                hover_focus=True,
                can_scroll=False,
                title="tic-tac-toe")
        self.state = state
        self.act_q = []

        self.cells = [[CellButton(mark=self.state.mark) for _ in range(3)] for _
                      in range(3)]
        layout = Layout([1, 1, 1], fill_frame=True)
        self.add_layout(layout)

        for x in range(3):
            for y in range(3):
                layout.add_widget(self.cells[x][y], x)

        self.fix()


renderer = FigletText(text="X", width=10)


def render_game(screen, scene):
    scenes = [Scene([GameView(screen, game_state)])]
    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


def run_game_view():
    last_scene = None
    while True:
        try:
            Screen.wrapper(render_game, arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene


if __name__ == '__main__':
    game_state = State()
    run_game_view()
