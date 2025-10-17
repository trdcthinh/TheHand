import pygame as pg

from thehand.core.configs import DEFAULT_WINDOW_SIZE


class State:
    def __init__(self) -> None:
        self.debug_mode = False
        self.display_flag = pg.NOFRAME
        self.window_size = DEFAULT_WINDOW_SIZE
        self.FPS = 60

        self.game_running = True

        self.sr_enable = True
        self.sr_running = False

        self.face_enable = True
        self.face_running = False

        self.hand_enable = True
        self.hand_running = False

        self.pose_enable = True
        self.pose_running = False
