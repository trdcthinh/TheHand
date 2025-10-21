import pygame as pg

import thehand as th


class HintScene(th.Scene):
    """Scene that shows a static background and a single hint line at the bottom corner.

    Accepts optional `background_path` (image file) and `hint_text`.
    """

    def __init__(
        self,
        state: th.State,
        store: th.Store,
        name: str,
        background_path: str | None = None,
        hint_text: str = "HINT",
        text_color: tuple[int, int, int] = th.COLOR_MOCHA_TEXT,
        align: str = "left",
    ) -> None:
        super().__init__(state, store, name)

        self.background_path = background_path
        self.hint_text = hint_text
        self.text_color = text_color
        self.align = align if align in ("left", "right") else "left"

        self.background: pg.Surface | None = None

    def setup(self) -> None:
        """Load and scale background image if provided."""
        if self.background_path:
            try:
                img = pg.image.load(self.background_path)
                self.background = pg.transform.scale(img, self.store.screen.get_size()).convert()
            except Exception as e:
                print(f"[HintScene] Không thể tải background: {e}")
                self.background = None

        self._start_timer = self.state.now

    def handle_events(self) -> None:
        for event in self.state.events:
            if event.type == pg.KEYDOWN and event.key in (pg.K_ESCAPE, pg.K_RETURN):
                pg.event.post(th.create_next_scene_event())

    def update(self) -> None:
        if self.state.now - self._start_timer > 5000:
            pg.event.post(th.create_next_scene_event())

    def render(self) -> None:
        screen = self.store.screen
        screen.fill(th.COLOR_MOCHA_CRUST)

        if self.background:
            screen.blit(self.background, (0, 0))

        font = self.store.font_text_32

        text_surface = font.render(self.hint_text, True, self.text_color)
        text_rect = text_surface.get_rect()
        padding = 60
        if self.align == "left":
            text_rect.bottomleft = (padding, screen.get_height() - padding)
        else:
            text_rect.bottomright = (screen.get_width() - padding, screen.get_height() - padding)

        screen.blit(text_surface, text_rect)
