import pygame as pg

from thehand.core.configs import DEFAULT_WINDOW_SIZE


class State:
    def __init__(self) -> None:
        self.debug_mode = False
        self.display_flag = pg.FULLSCREEN
        self.window_size = DEFAULT_WINDOW_SIZE

        self.FPS: int = 60
        self.vision_FPS: int = 10

        self.dt: float = 1 / self.FPS
        self.events: list[pg.event.Event] = []
        self.cursor = pg.SYSTEM_CURSOR_ARROW

        self.sys_font = pg.font.SysFont("Comic Sans MS", 24)
        self.display_font_lg = pg.font.Font("data/fonts/MajorMonoDisplay.ttf", 64)
        self.display_font_md = pg.font.Font("data/fonts/MajorMonoDisplay.ttf", 48)
        self.display_font_sm = pg.font.Font("data/fonts/MajorMonoDisplay.ttf", 32)
        self.text_font_lg = pg.font.Font("data/fonts/SpaceMono.ttf", 32)
        self.text_font_md = pg.font.Font("data/fonts/SpaceMono.ttf", 24)
        self.text_font_sm = pg.font.Font("data/fonts/SpaceMono.ttf", 18)

        self.sr_running = False
        self.face_running = False
        self.hand_running = False
        self.pose_running = False

        self.sounds = {
            "error": pg.mixer.Sound("data/audio/error.mp3"),
            "vine_boom": pg.mixer.Sound("data/audio/vine-boom.mp3"),
            "auughhh": pg.mixer.Sound("data/audio/auughhh.mp3"),
        }
