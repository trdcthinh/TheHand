from thehand.core import Camera, HandLandmarker


def main():
    camera = Camera()
    hand = HandLandmarker()

    while True:
        image = camera.read()
        if image:
            hand(image)


if __name__ == "__main__":
    main()
