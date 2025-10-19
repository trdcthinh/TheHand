from abc import ABC, abstractmethod

import pygame as pg

from thehand.core.state import State


class Scene(ABC):
    def __init__(
        self,
        name: str,
        screen: pg.Surface,
        state: State,
    ) -> None:
        self.name: str = name
        self.screen = screen
        self.state: State = state

        self.next_scene: str = ""

        self.have_setup = False
        self.done = False

    def __rshift__(self, other: "Scene") -> "Scene":
        self.next_scene = other.name
        return other

    @abstractmethod
    def setup(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle_events(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def render(self) -> None:
        raise NotImplementedError
