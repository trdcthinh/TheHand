from mediapipe.python.solutions import drawing_utils, drawing_styles, face_mesh
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks.python import vision, BaseOptions

import mediapipe as mp
import time
import cv2


class FaceLandmarker:
    def __init__(self, show_window: bool = False):
        self.show_window = show_window

        self.model = "models/face_landmarker.task"
        self.num_faces = 1
        self.min_face_detection_confidence = 0.5
        self.min_face_presence_confidence = 0.5
        self.min_tracking_confidence = 0.5

        self.counter = 0
        self.fps = 0
        self.start_time = time.time()
        self.detection_result = None
        self.fps_avg_frame_count = 10

        self.label_padding_width = 1500
        self.label_background_color = (255, 255, 255)

        base_options = BaseOptions(model_asset_path=self.model)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            num_faces=self.num_faces,
            min_face_detection_confidence=self.min_face_detection_confidence,
            min_face_presence_confidence=self.min_face_presence_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
            output_face_blendshapes=True,
            result_callback=self.result_callback,
        )
        self.detector = vision.FaceLandmarker.create_from_options(options)

    def result_callback(
        self,
        result: vision.FaceLandmarkerResult,
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

    def draw_landmarks(self, image, face_landmarks):
        face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        face_landmarks_proto.landmark.extend(
            [
                landmark_pb2.NormalizedLandmark(x=lm.x, y=lm.y, z=lm.z)
                for lm in face_landmarks
            ]
        )
        drawing_utils.draw_landmarks(
            image=image,
            landmark_list=face_landmarks_proto,
            connections=face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=drawing_styles.get_default_face_mesh_tesselation_style(),
        )
        drawing_utils.draw_landmarks(
            image=image,
            landmark_list=face_landmarks_proto,
            connections=face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=drawing_styles.get_default_face_mesh_contours_style(),
        )
        drawing_utils.draw_landmarks(
            image=image,
            landmark_list=face_landmarks_proto,
            connections=face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=drawing_styles.get_default_face_mesh_iris_connections_style(),
        )

    def draw_blendshapes(self, frame):
        legend_x = frame.shape[1] - self.label_padding_width + 20
        legend_y = 30
        bar_max_width = self.label_padding_width - 40
        bar_height = 8
        gap_between_bars = 5
        text_gap = 5

        face_blendshapes = self.detection_result.face_blendshapes
        if face_blendshapes:
            for idx, category in enumerate(face_blendshapes[0]):
                category_name = category.category_name
                score = round(category.score, 2)
                text = f"{category_name} ({score:.2f})"
                (text_width, _), _ = cv2.getTextSize(
                    text, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1
                )
                cv2.putText(
                    frame,
                    text,
                    (legend_x, legend_y + (bar_height // 2) + 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    (0, 0, 0),
                    1,
                    cv2.LINE_AA,
                )
                bar_width = int(bar_max_width * score)
                cv2.rectangle(
                    frame,
                    (legend_x + text_width + text_gap, legend_y),
                    (
                        legend_x + text_width + text_gap + bar_width,
                        legend_y + bar_height,
                    ),
                    (0, 255, 0),
                    -1,
                )
                legend_y += bar_height + gap_between_bars

    def draw_faces(self, image):
        if self.detection_result:
            for face_landmarks in self.detection_result.face_landmarks:
                self.draw_landmarks(image, face_landmarks)

            image = cv2.copyMakeBorder(
                image,
                0,
                0,
                0,
                self.label_padding_width,
                cv2.BORDER_CONSTANT,
                None,
                self.label_background_color,
            )
            self.draw_blendshapes(image)
        return image

    def __call__(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

        self.detector.detect_async(mp_image, time.time_ns() // 1_000_000)

        if not self.show_window:
            return

        self.draw_fps(image)
        output_image = self.draw_faces(image)

        cv2.imshow("Mediapipe Face Landmark", output_image)

    def close(self):
        self.detector.close()


if __name__ == "__main__":
    from time import sleep

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    landmarker = FaceLandmarker(True)

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
