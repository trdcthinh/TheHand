from thehand.engine.audition import Audition
from thehand.engine.state import StateManager


def main():
    state = StateManager()
    audition = Audition(state)
    audition()


if __name__ == "__main__":
    main()
