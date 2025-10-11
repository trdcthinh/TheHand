from vision.hand.hand import Hand
from enums import Command

import cv2


class Vision:
    def __init__(self):
        self.hand = Hand()

        self._camera = cv2.VideoCapture(0)
        self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.commands: list[Command]

    def __call__(self):
        if not self._camera.isOpened():
            return None

        success, image = self._cam.read()
        if not success:
            print("Camera not available")
            return None

        image = cv2.flip(image, 1)

        self.hand(image)
