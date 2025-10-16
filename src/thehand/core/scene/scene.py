from abc import ABC, abstractmethod
from typing import Self

import pygame

from thehand.core.state import State


class Scene(ABC):
    def __init__(
            self,
            name: str,
            screen: pygame.Surface,
            state: State,
    ) -> None:
        self.name: str = name
        self.screen = screen
        self.state: State = state

        self.next_scene: Self | None = None

    @abstractmethod
    def setup(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def render(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def cleanup(self) -> None:
        raise NotImplementedError

    def __rshift__(self, other: Self) -> Self:
        self.next_scene = other
        return other
