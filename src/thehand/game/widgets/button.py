from typing import Callable, Tuple

import pygame as pg

from thehand.core import Entity, State
from thehand.core.store import COLOR_MOCHA_BASE, COLOR_MOCHA_TEXT


class Button(Entity):
    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        state: State,
        text: str,
        click_callback: Callable[[], None] | None = None,
        font: pg.font.Font | None = None,
        color: Tuple[int, int, int] = COLOR_MOCHA_TEXT,
        hover_color: Tuple[int, int, int] = COLOR_MOCHA_TEXT,
        bg_color: Tuple[int, int, int] = COLOR_MOCHA_BASE,
        bg_opacity: float = 0.5,
        bg_hover_color: Tuple[int, int, int] = COLOR_MOCHA_BASE,
        bg_hover_opacity: float = 0.8,
    ) -> None:
        super().__init__(x, y, width, height)

        self.state = state

        self.text = text

        self.click_callback = click_callback

        self.font = self.state.text_font_md if font is None else font

        self.color = color

        self.hover_color = hover_color

        self.bg_color = bg_color

        self.bg_hover_color = bg_hover_color

        self.text_normal = self.font.render(self.text, True, self.color)

        self.text_hover = self.font.render(self.text, True, self.hover_color)

        self.text_rect = self.text_normal.get_rect(center=(self.x, self.y))

        self.bg_normal = pg.Surface((self.width, self.height))

        self.bg_normal.fill(self.bg_color)

        self.bg_normal.set_alpha(int(bg_opacity * 255))

        self.bg_hover = pg.Surface((self.width, self.height))

        self.bg_hover.fill(self.bg_hover_color)

        self.bg_hover.set_alpha(int(bg_hover_opacity * 255))

        self.rect = self.bg_normal.get_rect(center=(self.x, self.y))

        self._current_text = self.text_normal

        self._current_bg = self.bg_normal

    def setup(self):
        return

    def handle_events(self, mouse_pos: Tuple[int, int]) -> None:
        if (mouse_pos[0] in range(self.rect.left, self.rect.right)) and (
            mouse_pos[1] in range(self.rect.top, self.rect.bottom)
        ):
            self.current_text = self.text_hover

            self.current_bg = self.bg_hover

            self.state.cursor = pg.SYSTEM_CURSOR_HAND

        else:
            self.current_text = self.text_normal

            self.current_bg = self.bg_normal

            self.state.cursor = pg.SYSTEM_CURSOR_ARROW

    def update(self) -> None:
        return

    def render(self, surface: pg.Surface) -> None:
        surface.blit(self.current_bg, self.rect)

        surface.blit(self.current_text, self.text_rect)

    def check_for_click(self, mouse_pos: Tuple[int, int]) -> None:
        if (mouse_pos[0] in range(self.rect.left, self.rect.right)) and (
            mouse_pos[1] in range(self.rect.top, self.rect.bottom)
        ):
            if self.click_callback:
                self.click_callback()
