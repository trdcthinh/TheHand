from thehand.core import Audition, State


def example_sr_result_callback(text: str) -> None:
    print(f"{text} (*/ω＼*)")


class HelloAudition(Audition):
    def __init__(self, state: State) -> None:
        super().__init__(state)

        self.sr.set_result_callback(example_sr_result_callback)


def main():
    state = State()
    state.debug_mode = True

    audition = HelloAudition(state)
    audition()


if __name__ == "__main__":
    main()
