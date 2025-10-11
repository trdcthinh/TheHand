from vision.hand.hand import Hand
from vision.face.face import Face
from vision.pose.pose import Pose
from enums import Command
from time import sleep

import cv2


class Vision:
    def __init__(self, draw: bool = False):
        self.draw = draw

        self.hand = Hand(draw)
        self.face = Face(draw)
        self.pose = Pose(draw)

        self.commands: list[Command] = []

        self._camera = cv2.VideoCapture(0)
        self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    def __call__(self):
        while True:
            if not self._camera.isOpened():
                sleep(0.2)
                return None

            success, image = self._camera.read()
            if not success:
                print("Camera not available")
                return None

            image = cv2.flip(image, 1)

            command, hand_image = self.hand(image.copy())
            command, face_image = self.face(image.copy())
            command, pose_image = self.pose(image.copy())

            if self.draw:
                cv2.imshow("Vision", pose_image)
                if cv2.waitKey(50) == 27:
                    cv2.destroyAllWindows()
                    self.draw = False
