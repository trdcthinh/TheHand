import time

import cv2
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions, vision

from thehand.core.configs import NUM_POSE_DETECTED, POSE_LANDMARKER_MODEL
from thehand.core.types import PoseResultCallback


class PoseLandmarker:
    def __init__(self, result_callback: PoseResultCallback | None = None) -> None:
        self._result_callback = result_callback

        base_options = BaseOptions(model_asset_path=POSE_LANDMARKER_MODEL)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            num_poses=NUM_POSE_DETECTED,
            result_callback=self._mediapipe_result_callback,
        )
        self._landmarker = vision.PoseLandmarker.create_from_options(options)

    def __call__(self, image) -> None:
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        self._landmarker.detect_async(mp_image, time.time_ns() // 1_000_000)

    def set_result_callback(self, callback: PoseResultCallback) -> None:
        self._result_callback = callback

    def _mediapipe_result_callback(
        self, result: vision.PoseLandmarkerResult, _, timestamp_ms: int
    ) -> None:
        if self._result_callback:
            self._result_callback(result)
