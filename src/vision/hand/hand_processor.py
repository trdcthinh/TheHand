from vision.hand.hand_landmarker import HandLandmarker
from enums import Gesture, Command

import numpy as np


class HandProcessor:
    def __init__(self):
        self._landmarker = HandLandmarker()

        self._target_gestures: list[Gesture] = []

    def set_targets(self, targets: list[Gesture]):
        self._target_gestures = targets
        pass

    def landmark(self, img: np.ndarray) -> list:
        return self._landmarker(img)

    def classify(self, landmarks: list) -> Gesture:
        return Gesture.CAPTURE

    def process(self, landmarks: list) -> Command:
        return Command.DO_SOMETHING
