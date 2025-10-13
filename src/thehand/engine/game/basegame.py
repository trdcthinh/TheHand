from threading import Thread

from thehand.engine.audition import Audition
from thehand.engine.scene import SceneManager
from thehand.engine.state import StateManager
from thehand.engine.vision import Vision


class BaseGame:
    def __init__(self):
        self.state_manager = StateManager()
        self.have_setup = False

        self.scene_manager: SceneManager = None
        self.audition: Audition = None
        self.vision: Vision = None

    def setup(self) -> None:
        if self.have_setup:
            return None

        self.scene_manager = SceneManager()
        self.audition = Audition(self.state_manager)
        self.vision = Vision(self.state_manager)

    def run(self):
        self.setup()

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
