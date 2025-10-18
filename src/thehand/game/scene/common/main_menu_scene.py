import pygame as pg

from thehand.core import Scene, State


class MainMenuScene(Scene):
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
        for event in self.state.events:
            pass

    def update(self):
        return

    def render(self):
        self.screen.fill((25, 25, 25))
        text = self.state.display_font_lg.render(self.name, True, (240, 240, 240))
        self.screen.blit(text, (100, 100))
        pg.display.flip()
