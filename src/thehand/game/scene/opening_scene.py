import pygame as pg

from thehand.core import Scene, State
from thehand.core.event import create_next_scene_event


class OpeningScene(Scene):
    def handle_events(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pg.event.post(create_next_scene_event())

    def update(self):
        pass

    def render(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render('"Hello...?!"', True, (255, 255, 255))
        self.screen.blit(text, (100, 100))
        pg.display.flip()

    def __init__(
            self,
            name: str,
            screen: pg.Surface,
            state: State,
    ):
        super().__init__(name, screen, state)

        self.font = pg.font.SysFont("Comic Sans MS", 32)
