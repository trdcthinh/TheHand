import pygame as pg

from thehand.core import Scene, State
from thehand.core.event import create_next_scene_event


class BasicScene(Scene):
    def handle_events(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pg.event.post(create_next_scene_event(f"Request from {self.name}"))

    def update(self):
        self.gray = min(self.gray + 0.5, 255)

    def render(self):
        color = int(self.gray)
        self.screen.fill((color, color, color))
        pg.display.flip()

    def __init__(
        self,
        name: str,
        screen: pg.Surface,
        state: State,
    ):
        super().__init__(name, screen, state)

        self.gray = 0
