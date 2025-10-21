import cv2
import mediapipe as mp
import numpy as np
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks.python.vision.face_landmarker import (
    FaceLandmarkerResult,
)

import thehand as th

detection_result = None


def result_callback(result: FaceLandmarkerResult):
    global detection_result
    detection_result = result

    if not result.face_landmarks or len(result.face_landmarks) <= 0:
        return

    face_blendshapes = result.face_blendshapes[0]

    print(th.is_smile(face_blendshapes), th.get_smile_score(face_blendshapes))


def draw(rgb_image, detection_result):
    face_landmarks_list = detection_result.face_landmarks
    annotated_image = np.copy(rgb_image)

    for idx in range(len(face_landmarks_list)):
        face_landmarks = face_landmarks_list[idx]

        # Draw the face landmarks.
        face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        face_landmarks_proto.landmark.extend(
            [landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks]
        )

        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style(),
        )
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_contours_style(),
        )
        solutions.drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks_proto,
            connections=mp.solutions.face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_iris_connections_style(),
        )

    return annotated_image


def main():
    camera = th.Camera()
    hand = th.FaceLandmarker(result_callback)

    while True:
        image = camera.read()

        if image is None:
            continue

        hand(image)

        if not detection_result:
            continue

        annotated_image = draw(image, detection_result)

        cv2.imshow("Face", annotated_image)
        if cv2.waitKey(50) == 27:
            break


if __name__ == "__main__":
    main()
