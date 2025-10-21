from abc import ABC, abstractmethod

from .state import State
from .store import Store


class Entity(ABC):
    def __init__(self, state: State, store: Store):
        self.state = state
        self.store = store

    @abstractmethod
    def handle_events(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def render(self) -> None:
        raise NotImplementedError
