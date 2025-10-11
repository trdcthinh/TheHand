from engine.scene.scene_manager import SceneManager
from audition.audition import Audition
from vision.vision import Vision
from threading import Thread


class Game:
    def __init__(self):
        self.scene_manager = SceneManager()
        self.audition = Audition()
        self.vision = Vision()

    def __call__(self):
        audition_thread = Thread(target=self.run_audition, daemon=True)
        audition_thread.start()

        vision_thread = Thread(target=self.run_vision, daemon=True)
        vision_thread.start()

        self.run_game()

    def run_audition(self):
        self.audition()

    def run_vision(self):
        self.vision()

    def run_game(self):
        while True:
            self.scene_manager.run()
