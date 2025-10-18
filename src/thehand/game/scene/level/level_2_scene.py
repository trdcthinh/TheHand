import pygame as pg

from thehand.core import Scene, State


class Level02Scene(Scene):
    def __init__(
        self,
        name: str,
        screen: pg.Surface,
        state: State,
    ):
        super().__init__(name, screen, state)

    def setup(self):
        return

    def handle_events(self):
        return

    def update(self):
        return

    def render(self):
        self.screen.fill((25, 25, 25))
        text = self.state.text_font_md.render(self.name, True, (240, 240, 240))
        self.screen.blit(text, (100, 100))
        pg.display.flip()
