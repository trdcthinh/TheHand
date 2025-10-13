from thehand.game import ThehandGame


def main():
    game = ThehandGame()
    game.state.debug_mode = True
    game.run()


if __name__ == "__main__":
    main()
