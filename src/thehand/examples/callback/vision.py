import pygame as pg
from mediapipe.tasks.python.vision.hand_landmarker import HandLandmarkerResult

import thehand as th


def count_hand_callback(result: HandLandmarkerResult) -> None:
    hand_landmarks = result.hand_world_landmarks

    if hand_landmarks and len(hand_landmarks) > 0:
        th.print_inline(f"{len(hand_landmarks)} hands detected")
        th.create_number_event(len(hand_landmarks))


def dislike_quit_callback(result: HandLandmarkerResult) -> None:
    hand_landmarks = result.hand_world_landmarks

    for landmarks in hand_landmarks:
        if len(landmarks) < 21:
            continue

        dislike = th.is_hand_dislike(landmarks)
        if dislike:
            th.print_inline("You dislike our game?! T_T")
            pg.event.post(th.create_quit_event())
