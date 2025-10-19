import math

from mediapipe.tasks.python.components.containers.landmark import (
    Landmark,
    NormalizedLandmark,
)

from thehand.core.utils import print_inline


def testing(
    landmarks: list[Landmark], normalized_landmarks: list[NormalizedLandmark]
) -> bool:
    return True


def calculate_distance(lm1: Landmark, lm2: Landmark) -> float:
    return math.sqrt((lm2.x - lm1.x) ** 2 + (lm2.y - lm1.y) ** 2 + (lm2.z - lm1.z) ** 2)  # ty: ignore[unsupported-operator]


def calculate_angle_2d(initial: Landmark, terminal: Landmark) -> float:
    delta_x = terminal.x - initial.x  # ty: ignore[unsupported-operator]
    delta_y = terminal.y - initial.y  # ty: ignore[unsupported-operator]

    # Calculate the angle using atan2 (handles quadrants correctly)
    angle_radians = math.atan2(delta_y, delta_x)

    # Convert the angle to degrees
    angle_degrees = math.degrees(angle_radians)

    return angle_degrees


def calculate_angle_3d(lm1: Landmark, vertex: Landmark, lm2: Landmark) -> float:
    v1 = (lm1.x - vertex.x, lm1.y - vertex.y, lm1.z - vertex.z)  # ty: ignore[unsupported-operator]
    v2 = (lm2.x - vertex.x, lm2.y - vertex.y, lm2.z - vertex.z)  # ty: ignore[unsupported-operator]

    # Dot product of v1 and v2
    dot_product = v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

    # Magnitudes of v1 and v2
    magnitude_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2 + v1[2] ** 2)
    magnitude_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2 + v2[2] ** 2)

    # Avoid division by zero
    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0.0

    # Cosine of the angle
    cos_angle = dot_product / (magnitude_v1 * magnitude_v2)

    # Clamp the cosine value to the range [-1, 1] to avoid numerical errors
    cos_angle = max(-1.0, min(1.0, cos_angle))

    # Angle in radians
    angle_radians = math.acos(cos_angle)

    # Convert to degrees
    angle_degrees = math.degrees(angle_radians)

    return angle_degrees


def _normalized_to_pixel_coordinates(
    normalized_x: float, normalized_y: float, image_width: int, image_height: int
) -> None | tuple[int, int]:
    # Checks if the float value is between 0 and 1.
    def is_valid_normalized_value(value: float) -> bool:
        return (value > 0 or math.isclose(0, value)) and (
            value < 1 or math.isclose(1, value)
        )

    if not (
        is_valid_normalized_value(normalized_x)
        and is_valid_normalized_value(normalized_y)
    ):
        return None
    x_px = min(math.floor(normalized_x * image_width), image_width - 1)
    y_px = min(math.floor(normalized_y * image_height), image_height - 1)
    return x_px, y_px


def normalized_landmarks_to_coordinates(
    landmarks: NormalizedLandmark, image_width: int, image_height: int
) -> list[None | tuple[int, int]]:
    coordinates: list[None | tuple[int, int]] = [None] * 21

    for i, landmark in enumerate(landmarks):
        landmark_px = _normalized_to_pixel_coordinates(
            landmark.x, landmark.y, image_width, image_height
        )
        coordinates[i] = landmark_px

    return coordinates


def calculate_angle_on_screen(p1: tuple[int, int], p2: tuple[int, int]):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)

    return (angle_deg + 360) % 360


def get_hand_position_on_screen(
    normalized_landmarks: list[NormalizedLandmark],
    screen_width: int,
    screen_height: int,
) -> None | tuple[float, float]:
    coordinates = normalized_landmarks_to_coordinates(
        normalized_landmarks, screen_width, screen_height
    )

    if coordinates[9]:
        return (coordinates[9][0], coordinates[9][1])  # ty: ignore[invalid-return-type]

    return None


def is_hand_like(landmarks: list[Landmark]) -> bool:
    return (
        is_hand_horizontal(landmarks)
        and is_hand_horizontal_up(landmarks)
        and is_thumb_open(landmarks)
        and is_index_close(landmarks)
        and is_middle_close(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_close(landmarks)
    )


def is_hand_dislike(landmarks: list[Landmark]) -> bool:
    return (
        is_hand_horizontal(landmarks)
        and is_hand_horizontal_down(landmarks)
        and is_thumb_open(landmarks)
        and is_index_close(landmarks)
        and is_middle_close(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_close(landmarks)
    )


def is_hand_index(landmarks: list[Landmark]) -> bool:
    return (
        is_hand_vertical_up(landmarks)
        and not is_thumb_open(landmarks)
        and is_index_open(landmarks)
        and is_middle_close(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_close(landmarks)
    )


def is_hand_peace(landmarks: list[Landmark]) -> bool:
    return (
        is_hand_vertical_up(landmarks)
        and not is_thumb_open(landmarks)
        and is_index_open(landmarks)
        and is_middle_open(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_close(landmarks)
    )


def is_hand_gun(landmarks: list[Landmark]) -> bool:
    distance_8_12 = calculate_distance(landmarks[8], landmarks[12])
    distance_5_9 = calculate_distance(landmarks[5], landmarks[9])

    return (
        distance_8_12 * 0.7 < distance_5_9
        and is_index_open(landmarks)
        and is_middle_open(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_close(landmarks)
    )


def is_hand_four(landmarks: list[Landmark]) -> bool:
    return (
        is_hand_vertical_up(landmarks)
        and not is_thumb_open(landmarks)
        and is_index_open(landmarks)
        and is_middle_open(landmarks)
        and is_ring_open(landmarks)
        and is_pinky_open(landmarks)
    )


def is_hand_spider(landmarks: list[Landmark]) -> bool:
    return (
        is_thumb_open(landmarks)
        and is_index_open(landmarks)
        and is_middle_close(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_open(landmarks)
    )


def is_hand_call(landmarks: list[Landmark]) -> bool:
    return (
        is_thumb_open(landmarks)
        and is_index_close(landmarks)
        and is_middle_close(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_open(landmarks)
    )


def is_hand_v_capture(landmarks: list[Landmark]) -> bool:
    angle_4_5_8 = calculate_angle_3d(landmarks[4], landmarks[5], landmarks[8])
    return (
        int(angle_4_5_8) in range(75, 135)
        and is_thumb_open(landmarks)
        and is_index_open(landmarks)
        and is_middle_close(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_close(landmarks)
    )


def is_hand_punch(landmarks: list[Landmark]) -> bool:
    return (
        is_index_close(landmarks)
        and is_middle_close(landmarks)
        and is_ring_close(landmarks)
        and is_pinky_close(landmarks)
    )


def is_hand_vertical(landmarks: list[Landmark]) -> bool:
    angle_0_9 = calculate_angle_2d(landmarks[0], landmarks[9])
    return (int(angle_0_9) in range(45, 135)) or (angle_0_9 in range(-135, -45))


def is_hand_vertical_up(landmarks: list[Landmark]) -> bool:
    angle_0_9 = calculate_angle_2d(landmarks[0], landmarks[9])
    return int(angle_0_9) in range(-135, -45)


def is_hand_vertical_down(landmarks: list[Landmark]) -> bool:
    angle_0_9 = calculate_angle_2d(landmarks[0], landmarks[9])
    return int(angle_0_9) in range(45, 135)


def is_hand_horizontal(landmarks: list[Landmark]) -> bool:
    angle_5_17 = calculate_angle_2d(landmarks[5], landmarks[17])
    return (int(angle_5_17) in range(45, 135)) or (int(angle_5_17) in range(-135, -45))


def is_hand_horizontal_up(landmarks: list[Landmark]) -> bool:
    angle_5_17 = calculate_angle_2d(landmarks[5], landmarks[17])
    return int(angle_5_17) in range(45, 135)


def is_hand_horizontal_down(landmarks: list[Landmark]) -> bool:
    angle_5_17 = calculate_angle_2d(landmarks[5], landmarks[17])
    return int(angle_5_17) in range(-135, -45)


def is_thumb_open(landmarks: list[Landmark]) -> bool:
    angle_4_3_2 = calculate_angle_3d(landmarks[4], landmarks[3], landmarks[2])
    angle_4_2_0 = calculate_angle_3d(landmarks[4], landmarks[2], landmarks[0])
    return angle_4_3_2 > 150 and angle_4_2_0 > 150


def is_thumb_close(landmarks: list[Landmark]) -> bool:
    angle_4_3_2 = calculate_angle_3d(landmarks[4], landmarks[3], landmarks[2])
    angle_4_2_0 = calculate_angle_3d(landmarks[4], landmarks[2], landmarks[0])
    return angle_4_3_2 < 135 or angle_4_2_0 < 135


def is_index_open(landmarks: list[Landmark]) -> bool:
    angle_8_6_5 = calculate_angle_3d(landmarks[8], landmarks[6], landmarks[5])
    return angle_8_6_5 > 135


def is_index_close(landmarks: list[Landmark]) -> bool:
    distance_0_8 = calculate_distance(landmarks[0], landmarks[8])
    distance_0_9 = calculate_distance(landmarks[0], landmarks[9])
    return distance_0_8 * 0.8 < distance_0_9


def is_middle_open(landmarks: list[Landmark]) -> bool:
    angle_12_10_9 = calculate_angle_3d(landmarks[12], landmarks[10], landmarks[9])
    return angle_12_10_9 > 135


def is_middle_close(landmarks: list[Landmark]) -> bool:
    distance_0_12 = calculate_distance(landmarks[0], landmarks[12])
    distance_0_9 = calculate_distance(landmarks[0], landmarks[9])
    return distance_0_12 * 0.8 < distance_0_9


def is_ring_open(landmarks: list[Landmark]) -> bool:
    angle_16_14_13 = calculate_angle_3d(landmarks[16], landmarks[14], landmarks[13])
    return angle_16_14_13 > 135


def is_ring_close(landmarks: list[Landmark]) -> bool:
    distance_0_16 = calculate_distance(landmarks[0], landmarks[16])
    distance_0_9 = calculate_distance(landmarks[0], landmarks[9])
    return distance_0_16 * 0.8 < distance_0_9


def is_pinky_open(landmarks: list[Landmark]) -> bool:
    angle_20_18_17 = calculate_angle_3d(landmarks[20], landmarks[18], landmarks[17])
    return angle_20_18_17 > 135


def is_pinky_close(landmarks: list[Landmark]) -> bool:
    distance_0_20 = calculate_distance(landmarks[0], landmarks[20])
    distance_0_9 = calculate_distance(landmarks[0], landmarks[9])
    return distance_0_20 * 0.8 < distance_0_9
