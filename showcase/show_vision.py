from thehand.core.vision import Vision


def main():
    vision = Vision()
    vision.state.debug_mode = True
    vision()


if __name__ == "__main__":
    main()
