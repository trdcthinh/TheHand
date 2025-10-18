import pygame as pg
from mediapipe.tasks.python.components.containers.landmark import Landmark
from mediapipe.tasks.python.vision.face_landmarker import FaceLandmarkerResult
from mediapipe.tasks.python.vision.hand_landmarker import HandLandmarkerResult
from mediapipe.tasks.python.vision.pose_landmarker import PoseLandmarkerResult

from thehand.core.event import create_number_event, create_quit_event
from thehand.core.utils import print_inline
from thehand.core.vision.utils import (
    calculate_angle_3_point,
    calculate_angle_vector,
    calculate_distance,
    match_dislike,
)


def count_hand_callback(result: HandLandmarkerResult) -> None:
    hand_landmarks = result.hand_world_landmarks

    if hand_landmarks and len(hand_landmarks) > 0:
        print_inline(f"{len(hand_landmarks)} hands detected")
        create_number_event(len(hand_landmarks))


def dislike_quit_callback(result: HandLandmarkerResult) -> None:
    hand_landmarks = result.hand_world_landmarks

    for landmarks in hand_landmarks:
        if len(landmarks) < 21:
            continue

        dislike = match_dislike(landmarks)
        if dislike:
            print_inline("You dislike our game?! T_T")
            pg.event.post(create_quit_event())
