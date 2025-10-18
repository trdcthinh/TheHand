import pygame as pg

from thehand.core.configs import DEFAULT_WINDOW_SIZE


class State:
    def __init__(self) -> None:
        self.debug_mode = False
        self.display_flag = pg.NOFRAME
        self.window_size = DEFAULT_WINDOW_SIZE

        self.FPS = 60
        self.vision_FPS = 10

        self.events: list[pg.event.Event] = []

        self.sr_running = False
        self.face_running = False
        self.hand_running = False
        self.pose_running = False
