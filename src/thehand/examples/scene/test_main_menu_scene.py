import pygame as pg

from thehand.core import SpeechRecognition, State, Store
from thehand.game.scene.common.main_menu_scene import MainMenuScene


def main():
    pg.init()

    clock = pg.time.Clock()

    state = State()
    store = Store()
    sr = SpeechRecognition(state)

    store.screen = pg.display.set_mode(state.window_size)

    scene = MainMenuScene("MainMenu", state, store, sr)

    scene.setup()

    while not scene.done:
        state.events = pg.event.get()

        scene.handle_events()
        scene.update()
        scene.render()

        clock.tick(state.FPS)

    pg.quit()


if __name__ == "__main__":
    main()
