import time
from threading import Thread

import pygame as pg

from thehand.core import (
    SceneManager,
    State,
    FaceLandmarker,
    HandLandmarker,
    PoseLandmarker,
)
from thehand.core import SpeechRecognition
from thehand.game.callbacks import sr_hello_callback
from thehand.game.scene import OpeningScene, PlayScene


class TheHandGame:
    def __init__(self) -> None:
        self.state = State()

        self.scene_manager: SceneManager | None = None

        self.sr: SpeechRecognition | None = None

        self.face: FaceLandmarker | None = None
        self.hand: HandLandmarker | None = None
        self.pose: PoseLandmarker | None = None

        self.screen: pg.Surface | None = None

    def __call__(self) -> None:
        if not self.scene_manager:
            raise TypeError("SceneManager not initialized")

        scene_manager_thread = Thread(target=self.scene_manager.run, daemon=True)
        scene_manager_thread.start()

        # sr_thread = Thread(target=self.sr.run, daemon=True)
        # sr_thread.start()

        while self.state.game_running:
            time.sleep(0.2)

        print("End game!")
        self.sr.stop()
        # sr_thread.join()

        pg.quit()
        exit(0)

    def init(self) -> None:
        self.scene_manager = SceneManager(self.state)

        if self.state.sr_enable:
            self.sr = SpeechRecognition(self.state, sr_hello_callback)

        if self.state.face_enable:
            self.face = FaceLandmarker()
        if self.state.hand_enable:
            self.hand = HandLandmarker()
        if self.state.pose_enable:
            self.pose = PoseLandmarker()

        self.screen = pg.display.set_mode(
            self.state.window_size, self.state.display_flag
        )

        self.setup_scenes()

    def setup_scenes(self) -> None:
        opening_scene = OpeningScene("open", self.screen, self.state)
        play_scene = PlayScene("play", self.screen, self.state)

        opening_scene >> play_scene

        self.scene_manager += opening_scene
        self.scene_manager += play_scene

        self.scene_manager << opening_scene
