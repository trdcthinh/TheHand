import pygame as pg


from mediapipe.tasks.python.components.containers.landmark import Landmark


from mediapipe.tasks.python.vision.face_landmarker import FaceLandmarkerResult


from mediapipe.tasks.python.vision.hand_landmarker import HandLandmarkerResult


from mediapipe.tasks.python.vision.pose_landmarker import PoseLandmarkerResult


from thehand.core.event import create_next_scene_event


from thehand.core.vision.utils import (
    calculate_distance,
    calculate_angle_3_point,
    calculate_angle_vector,
    match_dislike,
)


def sr_hello_callback(text: str) -> None:
    print(f"\r{' ' * 80}\r{text.ljust(80)}", end="", flush=True)

    if "hello" in text.lower():
        print(f"\r{' ' * 80}\rRequest next scene", end="", flush=True)

        pg.event.post(create_next_scene_event())


def sr_close_callback(text: str) -> None:
    print(f"\r{' ' * 80}\r{text.ljust(80)}", end="", flush=True)

    if "close" in text.lower():
        print(f"\r{' ' * 80}\rRequest next scene", end="", flush=True)

        pg.event.post(create_next_scene_event())


def dislike_callback(result: HandLandmarkerResult):
    hand_landmarks = result.hand_world_landmarks

    if hand_landmarks and len(hand_landmarks) > 0:
        print(f"{len(hand_landmarks)} hands detected")

    for landmarks in hand_landmarks:
        dislike = match_dislike(landmarks)

        if dislike:
            print("DISLIKE!!!")
    return
