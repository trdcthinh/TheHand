import cv2

from thehand.core.configs import CAMERA_FRAME_SIZE


class Camera:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_FRAME_SIZE[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_FRAME_SIZE[1])

    def read(self):
        if not self.camera.isOpened():
            return None

        success, image = self.camera.read()
        if not success:
            print("Camera not available")
            return None

        return cv2.flip(image, 1)
