from mediapipe.python.solutions import drawing_utils, drawing_styles, hands
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks.python import vision, BaseOptions

import mediapipe as mp
import time
import cv2


class HandLandmarker:
    def __init__(self, show_window: bool = False):
        self.show_window = show_window

        self.model = "models/hand_landmarker.task"
        self.num_hands = 2
        self.min_hand_detection_confidence = 0.5
        self.min_hand_presence_confidence = 0.5
        self.min_tracking_confidence = 0.5

        self.counter = 0
        self.fps = 0
        self.start_time = time.time()
        self.detection_result = None
        self.fps_avg_frame_count = 10

        base_options = BaseOptions(model_asset_path=self.model)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            num_hands=self.num_hands,
            min_hand_detection_confidence=self.min_hand_detection_confidence,
            min_hand_presence_confidence=self.min_hand_presence_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
            result_callback=self.result_callback,
        )
        self.landmarker = vision.HandLandmarker.create_from_options(options)

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
        fps_text = f"FPS = {self.fps:.1f}"
        text_location = (20, 50)
        cv2.putText(
            image,
            fps_text,
            text_location,
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

    def __call__(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        self.landmarker.detect_async(mp_image, time.time_ns() // 1_000_000)

        if not self.show_window:
            return

        self.draw_fps(image)

        if self.detection_result:
            self.draw_hands(image)

        cv2.imshow("Mediapipe Hand Landmark", image)

    def close(self):
        self.landmarker.close()


if __name__ == "__main__":
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
        landmarker(img)

        if cv2.waitKey(50) == 27:
            break

    landmarker.close()
    camera.release()
    cv2.destroyAllWindows()
