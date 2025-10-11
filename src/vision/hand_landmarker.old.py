from mediapipe.python.solutions import drawing_styles
from mediapipe.python.solutions import drawing_utils
from mediapipe.python.solutions import hands
from imutils import resize

import numpy as np
import cv2


class HandLandmarker:
    def __init__(self, show_window: bool = False):
        self._show_window = show_window

        self.landmarker = hands.Hands(
            static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5
        )

        self._window_size = 1280, 720

        self._detection_result = None

    def __call__(self, img: np.ndarray) -> list | None:
        # Flip horizontal
        img = cv2.flip(img, 1)

        # Convert image to RGB for inference
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self._detection_result = self.landmarker.process(img_rgb)

        if self._show_window and self._detection_result.multi_hand_landmarks:
            self.draw(img)

        if self._show_window:
            resized_img = resize(img, self._window_size[0], self._window_size[1])
            cv2.imshow("Mediapipe Hand Landmark", resized_img)

        if cv2.waitKey(50) & 0xFF == 32:  # Limit 20FPS
            return None

    def draw(self, img: np.ndarray):
        for hand_landmarks in self._detection_result.multi_hand_landmarks:
            drawing_utils.draw_landmarks(
                img,
                hand_landmarks,
                hands.HAND_CONNECTIONS,
                drawing_styles.get_default_hand_landmarks_style(),
                drawing_styles.get_default_hand_connections_style(),
            )


if __name__ == "__main__":
    from time import sleep

    camera = cv2.VideoCapture(0)
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

        landmarker(img)
