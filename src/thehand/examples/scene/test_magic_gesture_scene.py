import pygame as pg
<<<<<<< HEAD
from thehand.game.scenes.level.Magic_gesture_scene import MagicGestureScene
=======

>>>>>>> b6c4f5e1f92c379e7209f53be54d43c50d1d168b
import thehand as th
from thehand.game.scenes.level.magic_gesture_scene import MagicGestureScene


def main():
    pg.init()
    state = th.State()
    screen = pg.display.set_mode(state.window_size)
    clock = pg.time.Clock()
    store = th.Store()  # hoặc None nếu không cần
    scene = MagicGestureScene("MagicGesture", state, store, screen)
    scene.setup()
    running = True
    while running:
        state.events = pg.event.get()
        scene.handle_events()
        scene.update()
        scene.render()
        clock.tick(state.FPS)
    pg.quit()


if __name__ == "__main__":
    main()
