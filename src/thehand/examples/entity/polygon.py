from typing import Tuple

import pygame as pg

from thehand.core import Entity

COLOR_BLUE = (0, 0, 255)


class RectangleEntity(Entity):
    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        color: Tuple[int, int, int] = COLOR_BLUE,
    ) -> None:
        super().__init__(x, y, width, height)
        self.color = color

        self.image.fill(self.color)

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pg.Surface) -> None:
        surface.blit(self.image, self.rect)
