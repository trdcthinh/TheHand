from vision.hand.hand_landmarker import HandLandmarker
from vision.hand.hand_processor import HandProcessor
from enums import Command


class Hand:
    def __init__(self):
        self._landmarker = HandLandmarker()
        self._processor = HandProcessor()

    def __call__(self, image):
        landmarks: list = self._landmarker(image)

        command: Command = self._processor(landmarks)

        return command
