import pygame as pg

from thehand.core.configs import DEFAULT_WINDOW_SIZE


class State:
    def __init__(self) -> None:
        self.debug_mode = False

        self.window_size = DEFAULT_WINDOW_SIZE
        self.display_flag = pg.FULLSCREEN

        self.FPS: int = 60
        self.vision_FPS: int = 10

        self.dt: float = 1 / self.FPS
        self.events: list[pg.event.Event] = []
        self.cursor = pg.SYSTEM_CURSOR_ARROW

        self.sr_running = False
        self.face_running = False
        self.hand_running = False
        self.pose_running = False
