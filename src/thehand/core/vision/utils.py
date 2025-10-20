import math

from mediapipe.tasks.python.components.containers.landmark import (
    Landmark,
    NormalizedLandmark,
)


def calculate_distance(lm1: Landmark, lm2: Landmark) -> float:
    return math.sqrt((lm2.x - lm1.x) ** 2 + (lm2.y - lm1.y) ** 2 + (lm2.z - lm1.z) ** 2)  # ty: ignore[unsupported-operator]


def calculate_angle_2d(initial: Landmark, terminal: Landmark) -> float:
    delta_x = terminal.x - initial.x  # ty: ignore[unsupported-operator]
    delta_y = terminal.y - initial.y  # ty: ignore[unsupported-operator]

    angle_radians = math.atan2(delta_y, delta_x)

    angle_degrees = math.degrees(angle_radians)

    return angle_degrees


def calculate_angle_3d(lm1: Landmark, vertex: Landmark, lm2: Landmark) -> float:
    v1 = (lm1.x - vertex.x, lm1.y - vertex.y, lm1.z - vertex.z)  # ty: ignore[unsupported-operator]
    v2 = (lm2.x - vertex.x, lm2.y - vertex.y, lm2.z - vertex.z)  # ty: ignore[unsupported-operator]

    dot_product = v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

    magnitude_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2 + v1[2] ** 2)
    magnitude_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2 + v2[2] ** 2)

    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0.0

    cos_angle = dot_product / (magnitude_v1 * magnitude_v2)
    cos_angle = max(-1.0, min(1.0, cos_angle))

    angle_radians = math.acos(cos_angle)
    angle_degrees = math.degrees(angle_radians)

    return angle_degrees


def normalized_to_pixel_coordinates(
    normalized_x: float, normalized_y: float, image_width: int, image_height: int
) -> None | tuple[int, int]:
    def is_valid_normalized_value(value: float) -> bool:
        return (value > 0 or math.isclose(0, value)) and (value < 1 or math.isclose(1, value))

    if not (is_valid_normalized_value(normalized_x) and is_valid_normalized_value(normalized_y)):
        return None

    x_px = min(math.floor(normalized_x * image_width), image_width - 1)
    y_px = min(math.floor(normalized_y * image_height), image_height - 1)

    return x_px, y_px


def normalized_landmarks_to_coordinates(
    normalized_landmarks: list[NormalizedLandmark], image_width: int, image_height: int
) -> list[None | tuple[int, int]]:
    coordinates: list[None | tuple[int, int]] = [None] * 21

    for i, landmark in enumerate(normalized_landmarks):
        landmark_px = normalized_to_pixel_coordinates(landmark.x, landmark.y, image_width, image_height)
        coordinates[i] = landmark_px

    return coordinates


def calculate_angle_on_screen(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)

    return (angle_deg + 360) % 360
