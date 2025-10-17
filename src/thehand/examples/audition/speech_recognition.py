from thehand.core import SpeechRecognition, State

translation_count = 0
translations: list[str] = []


def result_callback(text: str):
    global translation_count
    translation_count += 1
    translations.append(text)
    print(f"\r{' ' * 80}\r{text.rjust(80)}", end="", flush=True)


def main():
    state = State()

    sr = SpeechRecognition(state, result_callback)

    try:
        sr.run()
    except KeyboardInterrupt:
        sr.stop()
        print(f"\n{sr.get_caption()}")
        print(f"{translation_count} translation times")
        print("Translation sequence:")
        for text in translations:
            print(text)


if __name__ == "__main__":
    main()
