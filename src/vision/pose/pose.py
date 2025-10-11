from vision.pose.pose_landmarker import PoseLandmarker
from vision.pose.pose_processor import PoseProcessor
from enums import Command

import numpy as np


class Pose:
    def __init__(self, draw: bool = False):
        self.draw = draw

        self._landmarker = PoseLandmarker(draw)
        self._processor = PoseProcessor()

    def __call__(self, image) -> tuple[Command, np.ndarray]:
        detection_result, image = self._landmarker(image)

        if not detection_result:
            return Command.DO_NOTHING, image

        command: Command = self._processor(detection_result)

        return command, image
