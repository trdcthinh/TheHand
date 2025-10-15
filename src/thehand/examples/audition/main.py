from thehand.examples.audition.hello_audition import HelloAudition


def main():
    audition = HelloAudition()
    audition.state.debug_mode = True
    audition()


if __name__ == "__main__":
    main()
