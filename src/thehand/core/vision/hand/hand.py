import numpy as np

from thehand.core.enums import Command
from thehand.core.state import State
from thehand.core.vision.hand.hand_landmarker import HandLandmarker
from thehand.core.vision.hand.hand_processor import HandProcessor


class Hand:
    def __init__(self, state: State):
        self.state: State = state if isinstance(state, State) else State()

        self._landmarker = HandLandmarker(self.state)
        self._processor = HandProcessor()

    def __call__(self, image) -> tuple[Command, np.ndarray]:
        detection_result, image = self._landmarker(image)

        if not detection_result:
            return Command.DO_NOTHING, image

        command: Command = self._processor(detection_result)

        return command, image
