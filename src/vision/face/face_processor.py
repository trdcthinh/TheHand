from enums import Gesture, Command


class FaceProcessor:
    def __init__(self):
        self._target_gestures: list[Gesture] = []

    def __call__(self, landmarks: list) -> Command:
        return Command.DO_SOMETHING

    def set_targets(self, targets: list[Gesture]):
        self._target_gestures = targets
        pass

    def classify(self, landmarks: list) -> Gesture:
        return Gesture.CAPTURE
