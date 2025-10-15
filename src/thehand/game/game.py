from thehand.game.opening_scene import OpeningScene

from thehand.core import Game


class ThehandGame(Game):
    def __init__(self):
        super().__init__()

        self.op = OpeningScene("op", self.scene_manager.screen)
        self.scene_manager.add(self.op)
        self.scene_manager.set_current_scene("op")
