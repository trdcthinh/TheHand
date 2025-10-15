import time
from abc import ABC, abstractmethod
from threading import Thread

from thehand.core.audition import Audition
from thehand.core.scene import SceneManager
from thehand.core.state import State
from thehand.core.vision import Vision


class Game(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self.state: State = State()
        self.scene_manager: SceneManager = SceneManager(self.state)

        self.audition: Audition | None = None
        self.vision: Vision | None = None

    def __call__(self) -> None:
        scene_manager_thread = Thread(target=self.scene_manager(), daemon=True)
        scene_manager_thread.start()

        if self.audition is not None:
            audition_thread = Thread(target=self.audition(), daemon=True)
            audition_thread.start()

        if self.vision is not None:
            vision_thread = Thread(target=self.vision(), daemon=True)
            vision_thread.start()

        time.sleep(99999)
