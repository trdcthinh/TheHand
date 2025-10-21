import pygame as pg

import thehand as th


class Page(th.Entity):
    def __init__(
        self,
        state: th.State,
        store: th.Store,
        background: pg.Surface | None = None,
        text: str = "",
        sound: pg.Sound | None = None,
        duration: int = 3000,
    ) -> None:
        super().__init__(state, store)

        if self.background is not None:
            self.background = background
        else:
            self.background = pg.Surface(self.state.window_size)
            self.background.fill(th.COLOR_MOCHA_BASE)

        self.text = text
        self.sound = sound
        self.duration = duration

    def setup(self) -> None:
        return

    def handle_events(self) -> None:
        return

    def update(self) -> None:
        return

    def render(self) -> None:
        return
