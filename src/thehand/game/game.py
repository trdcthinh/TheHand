from threading import Thread

import pygame as pg

from thehand.core import (
    FaceLandmarker,
    HandLandmarker,
    PoseLandmarker,
    SceneManager,
    SpeechRecognition,
    State,
    Camera,
)
from thehand.core.event import Event, EventCode
from thehand.game.scene import OpeningScene, PlayScene


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
        if not self.scene_manager:
            raise TypeError("SceneManager is not initialized")

        scene_manager_thread = Thread(target=self.scene_manager.run, daemon=True)
        scene_manager_thread.start()

        if not self.sr:
            raise TypeError("SpeechRecognition is not initialized")

        sr_thread = Thread(target=self.sr.run, daemon=True)
        sr_thread.start()

        vision_thread = Thread(target=self._run_vision, daemon=True)
        vision_thread.start()

        while True:
            self._handle_events()
            self.clock.tick(20)

    def init(self) -> None:
        self.scene_manager = SceneManager(self.state)

        self.sr = SpeechRecognition(self.state)

        self.camera = Camera()
        self.face = FaceLandmarker()
        self.hand = HandLandmarker()
        self.pose = PoseLandmarker()

        self.screen = pg.display.set_mode(
            self.state.window_size, self.state.display_flag
        )

        self._setup_scenes()

    def quit(self) -> None:
        self.sr.stop()
        self.scene_manager.stop()
        pg.quit()
        exit(0)

    def _setup_scenes(self) -> None:
        opening_scene = OpeningScene(
            "open", self.screen, self.state, self.sr, self.hand
        )
        play_scene = PlayScene("play", self.screen, self.state, self.sr)

        opening_scene >> play_scene

        self.scene_manager += opening_scene
        self.scene_manager += play_scene

        self.scene_manager << opening_scene

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

    def _handle_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print("End game!")
                self.quit()

            if event.type == Event.COMMAND.value:
                if event.code == EventCode.COMMAND_NEXT_SCENE:
                    if not self.scene_manager.current_scene.next_scene:
                        print("End game!")
                        self.quit()
                    self.scene_manager.next()


def main():
    pg.init()
    pg.font.init()

    game = TheHandGame()

    game.state.debug_mode = True
    game.state.display_flag = pg.SHOWN
    game.state.sr_enable = True
    game.state.hand_enable = False
    game.state.face_enable = False
    game.state.pose_enable = False

    game.init()
    game()


if __name__ == "__main__":
    main()
