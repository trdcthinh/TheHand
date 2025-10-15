import math


def normalized_to_pixel_coordinates(
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


def landmarks_to_coordinates(
    landmark_list, image_width: int, image_height: int
) -> None | list[None | tuple[int, int]]:
    if not landmark_list:
        return None

    coordinates: list[None | tuple[int, int]] = [None] * 21

    for i, landmark in enumerate(landmark_list.landmark):
        if (landmark.HasField("visibility") and landmark.visibility < 0.5) or (
            landmark.HasField("presence") and landmark.presence < 0.5
        ):
            continue
        landmark_px = normalized_to_pixel_coordinates(
            landmark.x, landmark.y, image_width, image_height
        )
        coordinates[i] = landmark_px

    return coordinates


def calculate_angle(p1: tuple[int, int], p2: tuple[int, int]):
    """
    Calculates the angle in degrees between two points (x1, y1) and (x2, y2).
    The angle is measured counter-clockwise from the positive x-axis.
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)

    return (angle_deg + 360) % 360
