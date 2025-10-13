import numpy as np

from thehand.engine.enums import Command
from thehand.engine.vision.face.face_landmarker import FaceLandmarker
from thehand.engine.vision.face.face_processor import FaceProcessor


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
