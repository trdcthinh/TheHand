import time

from pygame import Clock

from thehand.core.state import State
from thehand.core.vision import Camera, FaceLandmarker, HandLandmarker, PoseLandmarker


class Vision:
    def __init__(self, state: State) -> None:
        self.state = state

        self.face = FaceLandmarker()
        self.hand = HandLandmarker()
        self.pose = PoseLandmarker()

        self._camera = Camera()
        self._clock = Clock()

    def __call__(self) -> None:
        while True:
            image = self._camera.read()

            if not image:
                time.sleep(0.2)

            if self.state.face_running:
                self.hand(image)
            if self.state.hand_running:
                self.hand(image)
            if self.state.pose_running:
                self.hand(image)
