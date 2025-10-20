from threading import Thread

import pygame as pg

from thehand.core import (
    Camera,
    Event,
    EventCode,
    FaceLandmarker,
    HandLandmarker,
    PoseLandmarker,
    SceneManager,
    SpeechRecognition,
    State,
    Store,
)
from thehand.game.config import GAME_NAME
from thehand.game.scene import (
    CreditScene,
    HintScene,
    MainMenuScene,
    PacmanScene,
    SplashScene,
    TutorialScene,
)


class TheHandGame:
    def __init__(self) -> None:
        pg.init()
        pg.font.init()
        pg.mixer.init()
        pg.display.set_caption(GAME_NAME)

        self.state = State()
        self.store = Store()

        self.clock = pg.Clock()
        self.vision_clock = pg.Clock()

        self.scene_manager: SceneManager | None = None

        self.sr: SpeechRecognition | None = None

        self.camera: Camera | None = None
        self.face: FaceLandmarker | None = None
        self.hand: HandLandmarker | None = None
        self.pose: PoseLandmarker | None = None

    def init(self) -> None:
        screen_info = pg.display.Info()

        self.state.window_size = (screen_info.current_w, screen_info.current_h)
        self.store.screen = pg.display.set_mode(
            self.state.window_size, self.state.display_flag
        )

        self.scene_manager = SceneManager(self.state, self.store)

        self.sr = SpeechRecognition(self.state)

        self.camera = Camera()
        self.face = FaceLandmarker()
        self.hand = HandLandmarker()
        self.pose = PoseLandmarker()

        self._setup_scenes()

    def run(self) -> None:
        if not self.scene_manager:
            raise TypeError("SceneManager is not initialized")

        sr_thread = Thread(target=self.sr.run, daemon=True)
        sr_thread.start()

        vision_thread = Thread(target=self._run_vision, daemon=True)
        vision_thread.start()

        while True:
            self._handle_events()
            self.scene_manager()
            self.clock.tick(self.state.FPS)

    def quit(self) -> None:
        self.sr.stop()
        pg.quit()

        print("\n\n\n" + " QUIT GAME ".center(80, "="))
        print("\n\n" + " Thank you for playing our game! ".center(80, "=") + "\n\n")

        exit(0)

    def _setup_scenes(self) -> None:
        splash_scene = SplashScene("splash", self.state, self.store)
        main_menu_scene = MainMenuScene("main_menu", self.state, self.store, self.sr)
        tutorial_scene = TutorialScene("tutorial", self.state, self.store)
        hint_pacman_scene = HintScene("hint_pacman", self.state, self.store)
        pacman_scene = PacmanScene("pacman", self.state, self.store, self.hand)
        credit_scene = CreditScene("credit", self.state, self.store)

        splash_scene >> main_menu_scene >> hint_pacman_scene
        # tutorial_scene >> main_menu_scene

        hint_pacman_scene >> pacman_scene

        (
            self.scene_manager
            + splash_scene
            + tutorial_scene
            + main_menu_scene
            + hint_pacman_scene
            + pacman_scene
            + credit_scene
        )

        self.scene_manager << splash_scene

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

            if event.type == Event.COMMAND.value:
                if event.code == EventCode.COMMAND_NEXT_SCENE:
                    self._next_scene()
                if event.code == EventCode.COMMAND_CHANGE_SCENE:
                    self._change_scene(event.value)

        if self.state.debug_mode:
            self._debug_handle_events()

    def _debug_handle_events(self) -> None:
        for event in self.state.events:
            if event.type == pg.K_KP_ENTER:
                self._next_scene()


def main():
    game = TheHandGame()

    game.state.debug_mode = True

    game.init()
    game.run()


if __name__ == "__main__":
    main()
