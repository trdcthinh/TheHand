from thehand.core import SpeechRecognition, State
from thehand.core.utils import print_inline

translation_count = 0
translations: list[str] = []


def result_callback(text: str):
    global translation_count
    translation_count += 1
    translations.append(text)
    print_inline(text)


def main():
    state = State()

    sr = SpeechRecognition(state, result_callback)

    try:
        sr.run()
    except KeyboardInterrupt:
        sr.stop()
        print(f"\n{' '.join(sr.captions)}")
        print(f"{translation_count} translation times")
        print("Translation sequence:")
        for text in translations:
            print(text)


if __name__ == "__main__":
    main()
