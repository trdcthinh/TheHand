from typing import Callable, TypedDict

import pygame as pg
from mediapipe.tasks.python.vision.face_landmarker import FaceLandmarkerResult
from mediapipe.tasks.python.vision.hand_landmarker import HandLandmarkerResult
from mediapipe.tasks.python.vision.pose_landmarker import PoseLandmarkerResult

type SrResultCallback = Callable[[str], None]

type FaceResultCallback = Callable[[FaceLandmarkerResult], None]
type HandResultCallback = Callable[[HandLandmarkerResult], None]
type PoseResultCallback = Callable[[PoseLandmarkerResult], None]


class StoryChunk(TypedDict, total=False):
    name: str
    image: pg.Surface
    sound: str
    text: str
    duration: int
