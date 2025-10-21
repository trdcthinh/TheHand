import cv2

from thehand.core.configs import DEFAULT_FRAME_SIZE


class Camera:
    def __init__(self):
        self._camera = cv2.VideoCapture(0)

        self._camera.set(cv2.CAP_PROP_FRAME_WIDTH, DEFAULT_FRAME_SIZE[0])
        self._camera.set(cv2.CAP_PROP_FRAME_HEIGHT, DEFAULT_FRAME_SIZE[1])

    def read(self):
        if not self._camera.isOpened():
            return None

        success, image = self._camera.read()
        if not success:
            print("Camera not available")
            return None

        return cv2.flip(image, 1)
