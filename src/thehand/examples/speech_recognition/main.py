import argparse

from thehand.core.audition import SpeechRecognition


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        help="Model to run.",
        default="moonshine/base",
        choices=["moonshine/base", "moonshine/tiny"],
    )
    return parser.parse_args()


translation_count = 0


def callback(text: str):
    global translation_count
    translation_count += 1


def main():
    args = parse_args()

    sr = SpeechRecognition(args.model, callback)
    sr.state.debug_mode = True

    try:
        sr.run()
    except KeyboardInterrupt:
        sr.stop()
        print(f"\n{sr.get_caption()}")
        print(f"{translation_count} translation times")


if __name__ == "__main__":
    main()
