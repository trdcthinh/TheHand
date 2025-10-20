import pygame as pg

from thehand.core import Scene, State, Store


class CreditScene(Scene):
    def __init__(self, name: str, state: State, store: Store):
        super().__init__(name, state, store)

    def setup(self):
        return

    def handle_events(self):
        return

    def update(self):
        return

    def render(self):
        self.store.screen.fill((25, 25, 25))
        text = self.store.font_text_24.render(self.name, True, (240, 240, 240))
        self.store.screen.blit(text, (100, 100))
        pg.display.flip()
