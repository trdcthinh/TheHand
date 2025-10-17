import math

from mediapipe.tasks.python.components.containers.landmark import Landmark


def calculate_distance(lm1: Landmark, lm2: Landmark) -> float:
    """
    Calculate the Euclidean distance between two landmarks.

    Args:
        lm1 (Landmark): The first landmark with x, y, z coordinates.
        lm2 (Landmark): The second landmark with x, y, z coordinates.

    Returns:
        float: The Euclidean distance between the two landmarks.
    """
    return math.sqrt((lm2.x - lm1.x) ** 2 + (lm2.y - lm1.y) ** 2 + (lm2.z - lm1.z) ** 2)  # ty: ignore[unsupported-operator]


def calculate_angle_vector(initial: Landmark, terminal: Landmark) -> float:
    """
    Calculate the angle of the target landmark relative to the root landmark in 2D space (x, y).

    Args:
        root (Landmark): The root landmark.
        target (Landmark): The target landmark.

    Returns:
        float: The angle in degrees between the two landmarks in the x-y plane.
    """
    # Calculate the difference in x and y coordinates
    delta_x = terminal.x - initial.x  # ty: ignore[unsupported-operator]
    delta_y = terminal.y - initial.y  # ty: ignore[unsupported-operator]

    # Calculate the angle using atan2 (handles quadrants correctly)
    angle_radians = math.atan2(delta_y, delta_x)

    # Convert the angle to degrees
    angle_degrees = math.degrees(angle_radians)

    return angle_degrees


def calculate_angle_3_point(lm1: Landmark, vertex: Landmark, lm2: Landmark) -> float:
    """
    Calculate the angle (in degrees) between three landmarks with lm2 as the root.

    Args:
        lm1 (Landmark): The first landmark.
        lm2 (Landmark): The root landmark.
        lm3 (Landmark): The third landmark.

    Returns:
        float: The angle in degrees between the three landmarks.
    """
    # Vector from lm2 to lm1
    v1 = (lm1.x - vertex.x, lm1.y - vertex.y, lm1.z - vertex.z)  # ty: ignore[unsupported-operator]
    # Vector from lm2 to lm3
    v2 = (lm2.x - vertex.x, lm2.y - vertex.y, lm2.z - vertex.z)  # ty: ignore[unsupported-operator]

    # Dot product of v1 and v2
    dot_product = v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

    # Magnitudes of v1 and v2
    magnitude_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2 + v1[2] ** 2)
    magnitude_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2 + v2[2] ** 2)

    # Avoid division by zero
    if magnitude_v1 == 0 or magnitude_v2 == 0:
        raise ValueError(
            "One of the vectors has zero magnitude, cannot calculate angle."
        )

    # Cosine of the angle
    cos_angle = dot_product / (magnitude_v1 * magnitude_v2)

    # Clamp the cosine value to the range [-1, 1] to avoid numerical errors
    cos_angle = max(-1.0, min(1.0, cos_angle))

    # Angle in radians
    angle_radians = math.acos(cos_angle)

    # Convert to degrees
    angle_degrees = math.degrees(angle_radians)

    return angle_degrees


def match_dislike(landmarks: list[Landmark]) -> bool:
    if (
        len(landmarks) < 21
        or not landmarks[20]
        or not landmarks[16]
        or not landmarks[12]
        or not landmarks[9]
        or not landmarks[8]
        or not landmarks[4]
        or not landmarks[1]
        or not landmarks[0]
    ):
        return False

    angle_0_9 = calculate_angle_vector(landmarks[0], landmarks[9])
    angle_1_4 = calculate_angle_vector(landmarks[1], landmarks[4])

    distance_0_8 = calculate_distance(landmarks[0], landmarks[8])
    distance_0_9 = calculate_distance(landmarks[0], landmarks[9])
    distance_0_12 = calculate_distance(landmarks[0], landmarks[12])
    distance_0_16 = calculate_distance(landmarks[0], landmarks[16])
    distance_0_20 = calculate_distance(landmarks[0], landmarks[20])

    return (
        int(angle_1_4) in range(45, 135)
        and int(angle_0_9) in range(-45, 45)
        and distance_0_8 < distance_0_9
        and distance_0_12 < distance_0_9
        and distance_0_16 < distance_0_9
        and distance_0_20 < distance_0_9
    )


def match_peace(landmarks: list[Landmark]) -> bool:
    if (
        len(landmarks) < 21
        or not landmarks[20]
        or not landmarks[16]
        or not landmarks[12]
        or not landmarks[9]
        or not landmarks[8]
        or not landmarks[4]
        or not landmarks[1]
        or not landmarks[0]
    ):
        return False

    angle_8_5_12 = calculate_angle_3_point(landmarks[8], landmarks[5], landmarks[12])

    angle_8_5_0 = calculate_angle_3_point(landmarks[8], landmarks[5], landmarks[0])
    angle_12_9_0 = calculate_angle_3_point(landmarks[12], landmarks[9], landmarks[0])
    angle_16_13_0 = calculate_angle_3_point(landmarks[16], landmarks[13], landmarks[0])
    angle_20_17_0 = calculate_angle_3_point(landmarks[20], landmarks[17], landmarks[0])

    return (
        angle_8_5_12 > 20
        and angle_8_5_0 > 135
        and angle_12_9_0 > 135
        and angle_16_13_0 < 90
        and angle_20_17_0 < 90
    )
