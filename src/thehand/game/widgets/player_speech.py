import pygame as pg

import thehand as th


class PlayerSpeech(th.Entity):
    def __init__(
        self,
        state: th.State,
        store: th.Store,
        pos: tuple[int, int] = (50, 50),
        font: pg.font.Font | None = None,
        color: tuple[int, int, int] = th.COLOR_MOCHA_TEXT,
        bg_color: tuple[int, int, int] = th.COLOR_MOCHA_BASE,
        bg_opacity: float = 0.75,
    ) -> None:
        super().__init__(state, store)

        self.pos = pos
        self.font = self.store.font_text_24 if font is None else font
        self.color = color
        self.bg_color = bg_color
        self.bg_opacity = bg_opacity

        self.text = ""

    def setup(self) -> None:
        return

    def handle_events(self) -> None:
        return

    def update(self) -> None:
        return

    def render(self) -> None:
        text_sur = self.font.render(self.text, True, self.color)
        self.store.screen.blit(text_sur, self.pos)
