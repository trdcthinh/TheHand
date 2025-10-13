from thehand.engine.vision import Vision
from thehand.engine.state import StateManager


def main():
    state = StateManager()
    state.debug_mode = True

    vision = Vision(state)
    vision()


if __name__ == "__main__":
    main()
