import time

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.framework.formats import landmark_pb2
from mediapipe.python.solutions import drawing_styles, drawing_utils, pose
from mediapipe.tasks.python import BaseOptions, vision

from thehand.core.state import State


class PoseLandmarker:
    def __init__(self, state: State):
        self.state: State = state if isinstance(state, State) else State()

        self.model = "models/pose_landmarker.task"
        self.num_poses = 1
        self.output_segmentation_masks = True

        self.counter = 0
        self.fps = 0
        self.start_time = time.time()
        self.detection_result = None
        self.fps_avg_frame_count = 10

        options = BaseOptions(model_asset_path=self.model)
        options = vision.PoseLandmarkerOptions(
            options=options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            num_poses=self.num_poses,
            output_segmentation_masks=self.output_segmentation_masks,
            result_callback=self.result_callback,
        )
        self.landmarker = vision.PoseLandmarker.create_from_options(options)

    def __call__(self, image) -> tuple[vision.PoseLandmarkerResult, np.ndarray]:
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        self.landmarker.detect_async(mp_image, time.time_ns() // 1_000_000)

        if self.state.debug_mode:
            self.draw_fps(image)
            self.draw_landmarks(image)
            image = self.draw_segmentation_mask(image)

        return self.detection_result, image

    def result_callback(
        self,
        result: vision.PoseLandmarkerResult,
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

    def draw_landmarks(self, image):
        if self.detection_result:
            for pose_landmarks in self.detection_result.pose_landmarks:
                pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
                pose_landmarks_proto.landmark.extend(
                    [
                        landmark_pb2.NormalizedLandmark(
                            x=landmark.x, y=landmark.y, z=landmark.z
                        )
                        for landmark in pose_landmarks
                    ]
                )
                drawing_utils.draw_landmarks(
                    image,
                    pose_landmarks_proto,
                    pose.POSE_CONNECTIONS,
                    drawing_styles.get_default_pose_landmarks_style(),
                )

    def draw_segmentation_mask(self, image):
        if self.output_segmentation_masks and self.detection_result:
            if self.detection_result.segmentation_masks is not None:
                segmentation_mask = self.detection_result.segmentation_masks[
                    0
                ].numpy_view()
                mask_image = np.zeros(image.shape, dtype=np.uint8)
                mask_image[:] = (100, 100, 0)
                condition = np.stack((segmentation_mask,) * 3, axis=-1) > 0.1
                visualized_mask = np.where(condition, mask_image, image)
                image = cv2.addWeighted(image, 0.5, visualized_mask, 0.5, 0)
        return image

    def close(self):
        self.landmarker.close()


def main():
    from time import sleep

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

    landmarker = PoseLandmarker(True)

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
                f"\r{' ' * 80}\rPose detected: {len(detection_result.pose_landmarks)}",
                end="",
                flush=True,
            )

        cv2.imshow("Mediapipe Pose Landmark", img)

        if cv2.waitKey(50) == 27:
            break

    landmarker.close()
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
