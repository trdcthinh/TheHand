from mediapipe.python.solutions import drawing_utils, drawing_styles, pose
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks.python import vision, BaseOptions

import mediapipe as mp
import numpy as np
import time
import cv2


class PoseLandmarker:
    def __init__(self, show_window: bool = False):
        self.show_window = show_window

        self.model = "models/pose_landmarker.task"
        self.num_poses = 1
        self.min_pose_detection_confidence = 0.5
        self.min_pose_presence_confidence = 0.5
        self.min_tracking_confidence = 0.5
        self.output_segmentation_masks = False

        self.counter = 0
        self.fps = 0
        self.start_time = time.time()
        self.detection_result = None
        self.fps_avg_frame_count = 10

        self.row_size = 50  # pixels
        self.left_margin = 24  # pixels
        self.text_color = (0, 0, 0)  # black
        self.font_size = 1
        self.font_thickness = 1
        self.overlay_alpha = 0.5
        self.mask_color = (100, 100, 0)  # cyan

        base_options = BaseOptions(model_asset_path=self.model)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            num_poses=self.num_poses,
            min_pose_detection_confidence=self.min_pose_detection_confidence,
            min_pose_presence_confidence=self.min_pose_presence_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
            output_segmentation_masks=self.output_segmentation_masks,
            result_callback=self.result_callback,
        )
        self.landmarker = vision.PoseLandmarker.create_from_options(options)

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
        fps_text = f"FPS = {self.fps:.1f}"
        text_location = (self.left_margin, self.row_size)
        cv2.putText(
            image,
            fps_text,
            text_location,
            cv2.FONT_HERSHEY_DUPLEX,
            self.font_size,
            self.text_color,
            self.font_thickness,
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
                mask_image[:] = self.mask_color
                condition = np.stack((segmentation_mask,) * 3, axis=-1) > 0.1
                visualized_mask = np.where(condition, mask_image, image)
                image = cv2.addWeighted(
                    image, self.overlay_alpha, visualized_mask, self.overlay_alpha, 0
                )
        return image

    def __call__(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        self.landmarker.detect_async(mp_image, time.time_ns() // 1_000_000)

        if not self.show_window:
            return

        self.draw_fps(image)
        self.draw_landmarks(image)
        output_image = self.draw_segmentation_mask(image)

        cv2.imshow("Mediapipe Pose Landmark", output_image)

    def close(self):
        self.landmarker.close()


if __name__ == "__main__":
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
        landmarker(img)

        if cv2.waitKey(50) == 27:
            break

    landmarker.close()
    camera.release()
    cv2.destroyAllWindows()
