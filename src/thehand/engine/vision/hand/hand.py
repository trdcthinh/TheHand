import numpy as np

from thehand.engine.enums import Command
from thehand.engine.vision.hand.hand_landmarker import HandLandmarker
from thehand.engine.vision.hand.hand_processor import HandProcessor


class Hand:
    def __init__(self, draw: bool = False):
        self.draw = draw

        self._landmarker = HandLandmarker(draw)
        self._processor = HandProcessor()

    def __call__(self, image) -> tuple[Command, np.ndarray]:
        detection_result, image = self._landmarker(image)

        if not detection_result:
            return Command.DO_NOTHING, image

        command: Command = self._processor(detection_result)

        return command, image
