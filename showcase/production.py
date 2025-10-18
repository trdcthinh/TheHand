import pygame as pg

from thehand import TheHandGame


def main():
    pg.init()
    pg.font.init()
    pg.display.set_caption("[GAME_NO_NAME]")

    game = TheHandGame()
    game.init()
    game()


if __name__ == "__main__":
    main()
