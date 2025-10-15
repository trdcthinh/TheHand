import time

import cv2
import imutils
import numpy as np

from thehand.core import configs
from thehand.core.state import State
from thehand.core.vision.face.face import Face
from thehand.core.vision.hand.hand import Hand
from thehand.core.vision.pose.pose import Pose


class Vision:
    def __init__(self, state: State | None = None):
        self.state: State = state if isinstance(state, State) else State()

        self.hand: Hand = Hand(self.state)
        self.face: Face = Face(self.state)
        self.pose: Pose = Pose(self.state)

        self._camera = cv2.VideoCapture(0)
        self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, configs.FRAME_SIZE[0])
        self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, configs.FRAME_SIZE[1])

    def __call__(self):
        while True:
            image = self.get()
            if not image:
                time.sleep(0.2)

            hand_command, hand_image = self.hand(image.copy())
            face_command, face_image = self.face(image.copy())
            pose_command, pose_image = self.pose(image.copy())

    def get(self) -> np.ndarray | None:
        if not self._camera.isOpened():
            return None

        success, image = self._camera.read()
        if not success:
            print("Camera not available")
            return None

        image = cv2.flip(image, 1)

        return image

    def draw(self, hand_image, pose_image, face_image):
        row = imutils.resize(
            cv2.hconcat([hand_image, pose_image]), configs.FRAME_SIZE[0]
        )
        stacked_img = cv2.vconcat(
            [row, imutils.resize(face_image, configs.FRAME_SIZE[0])]
        )

        cv2.imshow("Vision", stacked_img)
        if cv2.waitKey(50) == 27:
            cv2.destroyAllWindows()
            exit(0)
