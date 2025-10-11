from enum import Enum


class Command(Enum):
    DO_SOMETHING = 0
    DO_ANOTHER_THING = 1


class Pose(Enum):
    POSE_0 = 0
    POSE_1 = 1


class Gesture(Enum):
    CAPTURE = 0
    PEACE = 1
    GUN = 2


class Face(Enum):
    FACE_0 = 0
    FACE_1 = 1


class ProcessStatus(Enum):
    WAITING = 0
    IN_PROGRESS = 1
    FAILED = 2
    SUCCEED = 3
