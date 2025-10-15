from abc import ABC, abstractmethod
from typing import Any


class BaseTextProcessor(ABC):
    @abstractmethod
    def __call__(self, text: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def result_callback(self, result: Any) -> None:
        raise NotImplementedError
