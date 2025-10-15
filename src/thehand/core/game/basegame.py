from abc import ABC, abstractmethod
from threading import Thread

import pygame

from thehand.core.audition import BaseAudition
from thehand.core.scene import SceneManager
from thehand.core.state import StateManager
from thehand.core.vision import Vision


class BaseGame(ABC):
    @abstractmethod
    def __init__(self, audition: BaseAudition) -> None:
        pygame.init()

        self.state: StateManager = StateManager()

        self.scene_manager: SceneManager = SceneManager(self.state)
        self.audition: BaseAudition = audition
        self.vision: Vision = Vision(self.state)

    def run(self):
        audition_thread = Thread(target=self.audition(), daemon=True)
        audition_thread.start()

        vision_thread = Thread(target=self.vision(), daemon=True)
        vision_thread.start()

        while True:
            self.scene_manager.run()
