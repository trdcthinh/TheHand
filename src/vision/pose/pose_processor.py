from vision.pose.pose_landmarker import PoseLandmarker
from enums import Pose, Command

import numpy as np


class PoseProcessor:
    def __init__(self):
        self._landmarker = PoseLandmarker()

        self._target_gestures: list[Pose] = []

    def set_targets(self, targets: list[Pose]):
        self._target_gestures = targets
        pass

    def landmark(self, img: np.ndarray) -> list:
        return self._landmarker(img)

    def classify(self, landmarks: list) -> Pose:
        return Pose.CAPTURE

    def process(self, landmarks: list) -> Command:
        return Command.DO_SOMETHING
