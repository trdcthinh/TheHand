from abc import ABC, abstractmethod

from thehand.core.state import State
from thehand.core.store import Store


class Scene(ABC):
    def __init__(
        self,
        name: str,
        state: State,
        store: Store,
    ) -> None:
        self.name = name
        self.state = state
        self.store = store

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
