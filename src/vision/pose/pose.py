from vision.pose.pose_landmarker import PoseLandmarker
from vision.pose.pose_processor import PoseProcessor
from enums import Command


class Pose:
    def __init__(self):
        self._landmarker = PoseLandmarker()
        self._processor = PoseProcessor()

    def __call__(self):
        landmarks: list = self._landmarker()

        command: Command = self._processor(landmarks)

        return command
