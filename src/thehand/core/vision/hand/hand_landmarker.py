import time

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.framework.formats import landmark_pb2
from mediapipe.python.solutions import drawing_styles, drawing_utils, hands
from mediapipe.tasks.python import BaseOptions, vision

from thehand.core.state import StateManager


class HandLandmarker:
    def __init__(self, state: StateManager):
        self.state: StateManager = (
            state if isinstance(state, StateManager) else StateManager()
        )

        self.model = "models/hand_landmarker.task"
        self.num_hands = 2

        self.start_time = time.time()
        self.counter = 0
        self.fps = 0
        self.fps_avg_frame_count = 10
        self.detection_result = None

        base_options = BaseOptions(model_asset_path=self.model)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            num_hands=self.num_hands,
            result_callback=self.result_callback,
        )
        self.landmarker = vision.HandLandmarker.create_from_options(options)

    def __call__(self, image) -> tuple[vision.HandLandmarkerResult, np.ndarray]:
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        self.landmarker.detect_async(mp_image, time.time_ns() // 1_000_000)

        if self.state.debug_mode:
            self.draw_fps(image)
            self.draw_hands(image)

        return self.detection_result, image

    def run(self, image) -> tuple[vision.HandLandmarkerResult, np.ndarray]:
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        self.landmarker.detect_async(mp_image, time.time_ns() // 1_000_000)

        if self.state.debug_mode:
            self.draw_fps(image)
            self.draw_hands(image)

        return self.detection_result, image

    def result_callback(
        self,
        result: vision.HandLandmarkerResult,
        unused_output_image,
        timestamp_ms: int,
    ):
        if self.counter % self.fps_avg_frame_count == 0:
            self.fps = self.fps_avg_frame_count / (time.time() - self.start_time)
            self.start_time = time.time()
        self.detection_result = result
        self.counter += 1

    def draw_fps(self, image):
        cv2.putText(
            image,
            f"FPS = {self.fps:.1f}",
            (24, 50),
            cv2.FONT_HERSHEY_DUPLEX,
            1,
            (0, 0, 0),
            1,
            cv2.LINE_AA,
        )

    def draw_landmarks(self, image, hand_landmarks):
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend(
            [
                landmark_pb2.NormalizedLandmark(x=lm.x, y=lm.y, z=lm.z)
                for lm in hand_landmarks
            ]
        )
        drawing_utils.draw_landmarks(
            image,
            hand_landmarks_proto,
            hands.HAND_CONNECTIONS,
            drawing_styles.get_default_hand_landmarks_style(),
            drawing_styles.get_default_hand_connections_style(),
        )

    def draw_hands(self, image):
        if self.detection_result:
            for idx in range(len(self.detection_result.hand_landmarks)):
                hand_landmarks = self.detection_result.hand_landmarks[idx]
                handedness = self.detection_result.handedness[idx]
                self.draw_landmarks(image, hand_landmarks)
                height, width, _ = image.shape
                x_coordinates = [lm.x for lm in hand_landmarks]
                y_coordinates = [lm.y for lm in hand_landmarks]
                text_x = int(min(x_coordinates) * width)
                text_y = int(min(y_coordinates) * height) - 10
                cv2.putText(
                    image,
                    f"{handedness[0].category_name}",
                    (text_x, text_y),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1,
                    (88, 205, 54),
                    1,
                    cv2.LINE_AA,
                )

    def close(self):
        self.landmarker.close()


def main():
    from time import sleep

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    landmarker = HandLandmarker(True)

    while True:
        if not camera.isOpened():
            sleep(0.2)
            continue

        success, img = camera.read()
        if not success:
            print("Camera not available")
            sleep(0.2)
            continue

        img = cv2.flip(img, 1)
        detection_result, img = landmarker(img)

        if detection_result:
            print(
                f"\r{' ' * 80}\rHand detected: {len(detection_result.hand_landmarks)}",
                end="",
                flush=True,
            )

        cv2.imshow("Mediapipe Hand Landmark", img)

        if cv2.waitKey(50) == 27:
            break

    landmarker.close()
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
