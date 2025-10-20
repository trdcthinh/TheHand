import pygame as pg

from thehand.core.configs import DEFAULT_WINDOW_SIZE
from thehand.core.utils import asset_path


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
        self.display_font_lg = pg.font.Font(
            asset_path("fonts/MajorMonoDisplay.ttf"), 64
        )
        self.display_font_md = pg.font.Font(
            asset_path("fonts/MajorMonoDisplay.ttf"), 48
        )
        self.display_font_sm = pg.font.Font(
            asset_path("fonts/MajorMonoDisplay.ttf"), 32
        )
        self.text_font_lg = pg.font.Font(asset_path("fonts/SpaceMono.ttf"), 32)
        self.text_font_md = pg.font.Font(asset_path("fonts/SpaceMono.ttf"), 24)
        self.text_font_sm = pg.font.Font(asset_path("fonts/SpaceMono.ttf"), 18)

        self.sr_running = False
        self.face_running = False
        self.hand_running = False
        self.pose_running = False

        self.sounds = {
            "error": pg.mixer.Sound(asset_path("audio/error.mp3")),
            "vine_boom": pg.mixer.Sound(asset_path("audio/vine_boom.mp3")),
            "auughhh": pg.mixer.Sound(asset_path("audio/auughhh.mp3")),
        }
