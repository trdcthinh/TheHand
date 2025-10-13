# from threading import Thread

from thehand.engine import BaseGame


class DevelopmentGame(BaseGame):
    def __init__(self):
        super().__init__()

        self.state_manager.debug_mode = True
