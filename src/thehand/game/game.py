from threading import Thread

import pygame as pg

import thehand as th
from thehand.game.config import GAME_NAME
from thehand.game.scenes import (
    CreditScene,
    HintScene,
    MainMenuScene,
    PacmanScene,
    SplashScene,
)


class TheHandGame:
    def __init__(self) -> None:
        pg.init()
        pg.font.init()
        pg.mixer.init()
        pg.display.set_caption(GAME_NAME)

        self.state = th.State()
        self.store = th.Store()

        self.clock = pg.Clock()
        self.vision_clock = pg.Clock()

        self.scene_manager: th.SceneManager | None = None

        self.sr: th.SpeechRecognition | None = None

        self.camera: th.Camera | None = None
        self.face: th.FaceLandmarker | None = None
        self.hand: th.HandLandmarker | None = None
        self.pose: th.PoseLandmarker | None = None

    def init(self) -> None:
        self.store.screen = pg.display.set_mode(self.state.window_size, self.state.display_flag)

        self.scene_manager = th.SceneManager(self.state, self.store)

        self.sr = th.SpeechRecognition(self.state)

        self.camera = th.Camera()
        self.face = th.FaceLandmarker()
        self.hand = th.HandLandmarker()
        self.pose = th.PoseLandmarker()

        self._setup_scenes()

    def run(self) -> None:
        if not self.scene_manager:
            raise TypeError("SceneManager is not initialized")

        sr_thread = Thread(target=self.sr.run, daemon=True)
        sr_thread.start()

        vision_thread = Thread(target=self._run_vision, daemon=True)
        vision_thread.start()

        while True:
            self.state.now = pg.time.get_ticks()
            self._handle_events()
            self.scene_manager()
            self.state.dt = self.clock.tick(self.state.FPS)

    def quit(self) -> None:
        self.sr.stop()
        pg.quit()

        print("\n\n\n" + " QUIT GAME ".center(80, "="))
        print("\n\n" + " Thank you for playing our game! ".center(80, "=") + "\n\n")

        exit(0)

    def _create_and_add_scenes(self) -> None:
        self.splash_scene = SplashScene("splash", self.state, self.store)
        self.scene_manager += self.splash_scene

        self.main_menu_scene = MainMenuScene("main_menu", self.state, self.store, self.sr)
        self.scene_manager += self.main_menu_scene

        self.hint_pacman_scene = HintScene("hint_pacman", self.state, self.store)
        self.scene_manager += self.hint_pacman_scene

        self.pacman_scene = PacmanScene("pacman", self.state, self.store, self.hand)
        self.scene_manager += self.pacman_scene

        self.credit_scene = CreditScene("credit", self.state, self.store)
        self.scene_manager += self.credit_scene

    def _setup_scenes(self) -> None:
        self._create_and_add_scenes()

        self.splash_scene >> self.main_menu_scene >> self.hint_pacman_scene
        self.hint_pacman_scene >> self.pacman_scene >> self.credit_scene

        self.scene_manager << self.splash_scene

    def _run_vision(self) -> None:
        if not self.face:
            raise TypeError("FaceLandmarker is not initialized")
        if not self.hand:
            raise TypeError("HandLandmarker is not initialized")
        if not self.pose:
            raise TypeError("PoseLandmarker is not initialized")

        while True:
            image = self.camera.read()

            if image is None:
                continue

            if self.state.hand_running:
                self.hand(image)

            if self.state.face_running:
                self.face(image)

            if self.state.pose_running:
                self.pose(image)

            self.vision_clock.tick(self.state.vision_FPS)

    def _next_scene(self) -> None:
        success = self.scene_manager.next()
        if not success:
            print("Failed to get next scene. Quitting.")
            self.quit()

    def _change_scene(self, scene: str) -> None:
        success = self.scene_manager.set_current(scene)
        if not success:
            print(f"Failed to change to '{scene}' scene. Quitting.")
            self.quit()

    def _handle_events(self) -> None:
        self.state.events = pg.event.get()

        for event in self.state.events:
            if event.type == pg.QUIT:
                self.quit()

            if event.type == th.THEHAND_EVENT:
                if event.code == th.C_NEXT_SCENE:
                    self._next_scene()
                if event.code == th.C_CHANGE_SCENE:
                    self._change_scene(event.value)

        if self.state.debug_mode:
            self._debug_handle_events()

    def _debug_handle_events(self) -> None:
        for event in self.state.events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_TAB:
                    self._next_scene()


def main():
    game = TheHandGame()

    game.state.debug_mode = True
    game.state.window_size = (1280, 720)
    game.state.display_flag = pg.SHOWN

    game.init()
    game.run()


if __name__ == "__main__":
    main()
