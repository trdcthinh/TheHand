import cv2
import numpy as np
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks.python.vision.pose_landmarker import PoseLandmarkerResult

from thehand.core import Camera, PoseLandmarker
from thehand.core.vision import is_arm_joint_close

detection_result = None

MARGIN = 10
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54)


def result_callback(result: PoseLandmarkerResult):
    global detection_result
    detection_result = result

    if not result.pose_world_landmarks or len(result.pose_world_landmarks) <= 0:
        return

    pose_landmarks = result.pose_world_landmarks

    for i, landmarks in enumerate(pose_landmarks):
        if len(landmarks) < 21:
            continue

        res = is_arm_joint_close(landmarks)
        # print(res)


def draw(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    # Loop through the detected poses to visualize.
    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]

        # Draw the pose landmarks.
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend(
            [
                landmark_pb2.NormalizedLandmark(
                    x=landmark.x, y=landmark.y, z=landmark.z
                )
                for landmark in pose_landmarks
            ]
        )
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style(),
        )
    return annotated_image


def main():
    camera = Camera()
    hand = PoseLandmarker(result_callback)

    while True:
        image = camera.read()

        if image is None:
            continue

        hand(image)

        if not detection_result:
            continue

        annotated_image = draw(image, detection_result)

        cv2.imshow("Pose", annotated_image)
        if cv2.waitKey(50) == 27:
            break


if __name__ == "__main__":
    main()
