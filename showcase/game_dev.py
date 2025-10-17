import pygame as pg

from thehand import TheHandGame


def main():
    pg.init()
    pg.font.init()

    game = TheHandGame()

    game.state.debug_mode = True
    game.state.display_flag = pg.SHOWN
    game.state.sr_enable = True
    game.state.hand_enable = False
    game.state.face_enable = False
    game.state.pose_enable = False

    game.init()
    game()


if __name__ == "__main__":
    main()
