import pygame as pg
from thehand.core import State
from thehand.game.scene.common.main_menu_scene import MainMenuScene

def main():
    pg.init()
    state = State()
    screen = pg.display.set_mode(state.window_size)
    clock = pg.time.Clock()
    scene = MainMenuScene("MainMenu", screen, state)
    scene.setup()
    running = True
    while running and not scene.done:
        state.events = pg.event.get()
        scene.handle_events()
        scene.update()
        scene.render()
        clock.tick(state.FPS)
        if scene.done:
            running = False
    pg.quit()

if __name__ == "__main__":
    main()
