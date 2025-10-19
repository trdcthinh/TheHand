from abc import ABC, abstractmethod

import pygame as pg


class Entity(ABC):
    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
    ):
        self.x: float = x
        self.y: float = y
        self.width: int = width
        self.height: int = height

    @abstractmethod
    def setup(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle_events(self, events: list[pg.Event]) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def render(self) -> None:
        raise NotImplementedError
