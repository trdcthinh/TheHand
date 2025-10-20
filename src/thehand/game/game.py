from threading import Thread

import pygame as pg

from thehand.core import (
    Camera,
    FaceLandmarker,
    HandLandmarker,
    PoseLandmarker,
    SceneManager,
    SpeechRecognition,
    State,
)
from thehand.core.event import Event, EventCode
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
        self.state = State()

        self.clock = pg.Clock()
        self.vision_clock = pg.Clock()

        self.scene_manager: SceneManager | None = None

        self.sr: SpeechRecognition | None = None

        self.camera: Camera | None = None
        self.face: FaceLandmarker | None = None
        self.hand: HandLandmarker | None = None
        self.pose: PoseLandmarker | None = None

        self.screen: pg.Surface | None = None

    def __call__(self) -> None:
        sr_thread = Thread(target=self.sr.run, daemon=True)
        sr_thread.start()

        vision_thread = Thread(target=self._run_vision, daemon=True)
        vision_thread.start()

        while True:
            self._handle_events()
            self.scene_manager()
            self.clock.tick(self.state.FPS)

    def init(self) -> None:
        self.scene_manager = SceneManager(self.state)

        self.sr = SpeechRecognition(self.state)

        self.camera = Camera()
        self.face = FaceLandmarker()
        self.hand = HandLandmarker()
        self.pose = PoseLandmarker()

        screen_info = pg.display.Info()
        self.state.window_size = (screen_info.current_w, screen_info.current_h)
        self.screen = pg.display.set_mode(
            self.state.window_size, self.state.display_flag
        )

        self._setup_scenes()

    def quit(self) -> None:
        self.sr.stop()
        pg.quit()
        print("\n\n\n" + " QUIT GAME ".center(80, "="))
        print("\n\n" + " Thank you for playing our game! ".center(80, "=") + "\n\n")
        exit(0)

    def _setup_scenes(self) -> None:
        splash_scene = SplashScene("splash", self.screen, self.state)
        main_menu_scene = MainMenuScene("main_menu", self.screen, self.state)
        tutorial_scene = TutorialScene("tutorial", self.screen, self.state)
        hint_pacman_scene = HintScene("hint_pacman", self.screen, self.state)
        pacman_scene = PacmanScene("pacman", self.screen, self.state, self.hand)
        credit_scene = CreditScene("credit", self.screen, self.state)

        splash_scene >> main_menu_scene >> tutorial_scene
        tutorial_scene >> main_menu_scene

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

            self.hand(image)

            self.vision_clock.tick(self.state.vision_FPS)

    def _next_scene(self) -> None:
        success = self.scene_manager.next()
        if not success:
            self.quit()

    def _handle_events(self) -> None:
        self.state.events = pg.event.get()

        for event in self.state.events:
            if event.type == pg.QUIT:
                self.quit()

            if event.type == pg.MOUSEBUTTONUP:
                self._next_scene()

            if event.type == Event.COMMAND.value:
                if event.code == EventCode.COMMAND_NEXT_SCENE:
                    self._next_scene()


def main():
    pg.init()
    pg.font.init()
    pg.display.set_caption("[GAME_NO_NAME]")

    game = TheHandGame()

    game.state.debug_mode = True

    game.init()
    game()


if __name__ == "__main__":
    main()
