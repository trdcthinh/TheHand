from mediapipe.tasks.python.components.containers.landmark import (
    Landmark,
    NormalizedLandmark,
)

from thehand.core.vision.utils import (
    calculate_angle_2d,
    calculate_angle_3d,
    calculate_distance,
    normalized_landmarks_to_coordinates,
)


def is_arm_joint_close(landmarks: list[Landmark]) -> tuple[bool, bool]:
    distance_11_12 = calculate_distance(landmarks[11], landmarks[12])

    distance_12_16 = calculate_distance(landmarks[12], landmarks[16])
    distance_11_15 = calculate_distance(landmarks[11], landmarks[15])

    print(
        f"{distance_11_15 / distance_11_12:.3f} {distance_12_16 / distance_11_12:.3f}"
    )

    left_arm_close = distance_11_15 < 45
    right_arm_close = distance_12_16 < 45

    return (left_arm_close, right_arm_close)
