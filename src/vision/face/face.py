from vision.face.face_landmarker import FaceLandmarker
from vision.face.face_processor import FaceProcessor
from enums import Command


import numpy as np


class Face:
    def __init__(self, draw: bool = False):
        self.draw = draw

        self._landmarker = FaceLandmarker(draw)
        self._processor = FaceProcessor()

    def __call__(self, image) -> tuple[Command, np.ndarray]:
        detection_result, image = self._landmarker(image)

        if not detection_result:
            return Command.DO_NOTHING, image

        command: Command = self._processor(detection_result)

        return command, image
