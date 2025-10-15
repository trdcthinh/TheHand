from thehand.core.audition import SpeechRecognition

translation_count = 0
translations: list[str] = []


def result_callback(text: str):
    global translation_count
    translation_count += 1
    translations.append(text)


def main():
    sr = SpeechRecognition(result_callback=result_callback)
    sr.state.debug_mode = True

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
