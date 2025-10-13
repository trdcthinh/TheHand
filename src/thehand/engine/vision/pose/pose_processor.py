from thehand.engine.enums import Command, Pose


class PoseProcessor:
    def __init__(self):
        self._target_gestures: list[Pose] = []

    def __call__(self, landmarks: list) -> Command:
        return Command.DO_NOTHING

    def set_targets(self, targets: list[Pose]):
        self._target_gestures = targets
        pass

    def classify(self, landmarks: list) -> Pose:
        return Pose.POSE_0
