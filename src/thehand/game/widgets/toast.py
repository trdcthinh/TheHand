from typing import Tuple

import pygame as pg

from thehand.core import Entity, State
from thehand.core.store import COLOR_MOCHA_BASE, COLOR_MOCHA_TEXT


class Toast(Entity):
    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        state: State,
        text: str,
        duration: int = 3000,  # in milliseconds
        font: pg.font.Font | None = None,
        color: Tuple[int, int, int] = COLOR_MOCHA_TEXT,
        bg_color: Tuple[int, int, int] = COLOR_MOCHA_BASE,
        bg_opacity: float = 0.8,
    ) -> None:
        super().__init__(x, y, width, height)
        self.state = state
        self.text = text
        self.duration = duration
        self.font = self.state.text_font_md if font is None else font
        self.color = color
        self.bg_color = bg_color
        self.bg_opacity = bg_opacity

        self.alpha = 0
        self.scale = 0.5
        self.animation_state = "HIDDEN"  # HIDDEN, FADE_IN, VISIBLE, FADE_OUT
        self.start_time = 0

    def setup(self) -> None:
        pass

    def handle_events(self, events: list[pg.Event]) -> None:
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

    def render(self, surface: pg.Surface) -> None:
        if self.animation_state != "HIDDEN":
            scaled_width = int(self.width * self.scale)
            scaled_height = int(self.height * self.scale)

            bg_surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
            bg_surface.fill(self.bg_color)
            bg_surface.set_alpha(self.alpha)

            text_surface = self.font.render(self.text, True, self.color)
            text_rect = text_surface.get_rect(center=(self.width / 2, self.height / 2))
            bg_surface.blit(text_surface, text_rect)

            scaled_bg = pg.transform.scale(bg_surface, (scaled_width, scaled_height))
            rect = scaled_bg.get_rect(center=(self.x, self.y))

            surface.blit(scaled_bg, rect)

    def show(self) -> None:
        self.animation_state = "FADE_IN"
        self.start_time = pg.time.get_ticks()
