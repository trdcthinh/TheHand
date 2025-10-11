from vision.face.face_landmarker import FaceLandmarker
from vision.face.face_processor import FaceProcessor
from enums import Command


class Face:
    def __init__(self):
        self._landmarker = FaceLandmarker()
        self._processor = FaceProcessor()

    def __call__(self):
        landmarks: list = self._landmarker()

        command: Command = self._processor(landmarks)

        return command
