from thehand.core import HandLandmarker, Camera


def main():
    camera = Camera()
    hand = HandLandmarker()

    while True:
        image = camera.read()
        if image:
            hand(image)


if __name__ == "__main__":
    main()
