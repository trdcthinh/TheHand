from mediapipe.tasks.python.components.containers.category import Category
from mediapipe.tasks.python.vision.face_landmarker import Blendshapes


def get_smile_score(blendshapes: list[Category]) -> float:
    return (
        blendshapes[Blendshapes.MOUTH_SMILE_LEFT].score
        + blendshapes[Blendshapes.MOUTH_SMILE_RIGHT].score  # ty: ignore[unsupported-operator]
    ) / 2


def is_smile(blendshapes: list[Category]) -> bool:
    score = get_smile_score(blendshapes)
    return score > 0.35
