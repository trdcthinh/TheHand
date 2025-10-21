import pygame as pg

import thehand as th


class Toast(th.Entity):
    def __init__(
            self,
            state: th.State,
            store: th.Store,
            pos: tuple[int, int],
            size: tuple[int, int],
            text: str,
            duration: int = 3000,
            font: pg.font.Font | None = None,
            color: tuple[int, int, int] = th.COLOR_MOCHA_TEXT,
            bg_color: tuple[int, int, int] = th.COLOR_MOCHA_BASE,
            bg_opacity: float = 0.8,
    ) -> None:
        super().__init__(state, store)

        self.pos = pos
        self.size = size
        self.text = text
        self.duration = duration
        self.font = self.store.font_text_24 if font is None else font
        self.color = color
        self.bg_color = bg_color
        self.bg_opacity = bg_opacity

        self.alpha = 0
        self.scale = 0.5
        self.animation_state = "HIDDEN"  # HIDDEN, FADE_IN, VISIBLE, FADE_OUT
        self.start_time = 0

    def setup(self) -> None:
        pass

    def handle_events(self) -> None:
        pass

    def update(self) -> None:
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.start_time

        if self.animation_state == "FADE_IN":
            if elapsed_time < 500:
                self.alpha = int((elapsed_time / 500) * 255 * self.bg_opacity)
                self.scale = 0.5 + (elapsed_time / 500) * 0.5
            else:
                self.alpha = int(255 * self.bg_opacity)
                self.scale = 1.0
                self.animation_state = "VISIBLE"
                self.start_time = current_time
        elif self.animation_state == "VISIBLE":
            if elapsed_time > self.duration:
                self.animation_state = "FADE_OUT"
                self.start_time = current_time
        elif self.animation_state == "FADE_OUT":
            if elapsed_time < 500:
                self.alpha = int((1 - (elapsed_time / 500)) * 255 * self.bg_opacity)
                self.scale = 1.0 - (elapsed_time / 500) * 0.5
            else:
                self.alpha = 0
                self.scale = 0.5
                self.animation_state = "HIDDEN"

    def render(self) -> None:
        if self.animation_state != "HIDDEN":
            scaled_width = int(self.size[0] * self.scale)
            scaled_height = int(self.size[1] * self.scale)

            bg_surface = pg.Surface((self.size[0], self.size[1]), pg.SRCALPHA)
            bg_surface.fill(self.bg_color)
            bg_surface.set_alpha(self.alpha)

            text_surface = self.font.render(self.text, True, self.color)
            text_rect = text_surface.get_rect(center=(self.size[0] / 2, self.size[1] / 2))
            bg_surface.blit(text_surface, text_rect)

            scaled_bg = pg.transform.scale(bg_surface, (scaled_width, scaled_height))
            rect = scaled_bg.get_rect(center=self.pos)

            self.store.screen.blit(scaled_bg, rect)

    def show(self) -> None:
        self.animation_state = "FADE_IN"
        self.start_time = pg.time.get_ticks()
