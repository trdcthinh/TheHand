from abc import ABC, abstractmethod

import pygame

COLOR_PINK = (255, 0, 255)


class Entity(ABC):
    """
    Abstract Base Class for all game entities (objects) in a Pygame project.

    Every concrete entity must implement the 'update' and 'draw' methods.
    """

    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        image: pygame.Surface | None = None,
    ):
        """
        Initializes the Entity with basic properties.

        :param x: Initial X coordinate (can be float for sub-pixel movement).
        :param y: Initial Y coordinate (can be float for sub-pixel movement).
        :param width: Width of the entity's bounding box.
        :param height: Height of the entity's bounding box.
        :param image: Optional Pygame Surface to represent the entity visually.
        """
        self.x: float = x
        self.y: float = y
        self.width: int = width
        self.height: int = height

        self.image: pygame.Surface = (
            image if image is not None else self._create_placeholder_surface()
        )

        self.rect: pygame.Rect = pygame.Rect(
            int(self.x), int(self.y), self.width, self.height
        )

    def _create_placeholder_surface(self) -> pygame.Surface:
        """Creates a simple placeholder surface if no image is provided."""
        surf = pygame.Surface((self.width, self.height))
        surf.fill(COLOR_PINK)
        return surf

    @abstractmethod
    def update(self, dt: float):
        """
        Abstract method to update the entity's state (e.g., position, animation).

        :param dt: Delta time, the time elapsed since the last frame (in seconds).
                   Essential for frame-rate independent movement.
        """
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface):
        """
        Abstract method to draw the entity onto the game screen/surface.

        :param surface: The Pygame Surface to draw the entity onto.
        """
        pass
