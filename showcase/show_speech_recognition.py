from thehand.engine.audition import SpeechRecognition

translation_count = 0


def callback(text: str):
    global translation_count
    translation_count += 1


def main():
    model = "moonshine/base"
    sr = SpeechRecognition(model, callback)

    try:
        sr.run()
    except KeyboardInterrupt:
        sr.stop()
        print(f"\n{sr.get_caption()}")
        print(f"{translation_count} translation times")


if __name__ == "__main__":
    main()
