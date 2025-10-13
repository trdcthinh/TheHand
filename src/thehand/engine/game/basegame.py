from threading import Thread

import pygame

from thehand.engine.audition import Audition
from thehand.engine.scene import SceneManager
from thehand.engine.state import StateManager
from thehand.engine.vision import Vision


class BaseGame:
    def __init__(self):
        pygame.init()

        self.state: StateManager = StateManager()
        self.scene_manager: SceneManager = SceneManager()
        self.audition: Audition = Audition(self.state)
        self.vision: Vision = Vision(self.state)

    def run(self):
        audition_thread = Thread(target=self._run_audition, daemon=True)
        audition_thread.start()

        vision_thread = Thread(target=self._run_vision, daemon=True)
        vision_thread.start()

        self._run_game()

    def _run_audition(self):
        self.audition()

    def _run_vision(self):
        self.vision()

    def _run_game(self):
        while True:
            self.scene_manager.run()
