from thehand.examples.audition.hello_audition import HelloAudition


def main():
    basic_audition = HelloAudition()
    basic_audition.state.debug_mode = True
    basic_audition()


if __name__ == "__main__":
    main()
