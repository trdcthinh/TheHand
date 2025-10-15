from typing import Tuple

import pygame

from thehand.core.configs import COLOR_BLUE
from thehand.core.entity import Entity


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

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
