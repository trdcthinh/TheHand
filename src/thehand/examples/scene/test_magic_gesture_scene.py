import pygame as pg
from thehand.core import State, Store
from thehand.game.scene.level.Magic_gesture_scene import MagicGestureScene

def main():
    pg.init()
    state = State()
    screen = pg.display.set_mode(state.window_size)
    clock = pg.time.Clock()
    store = Store()  # hoặc None nếu không cần
    scene = MagicGestureScene("MagicGesture", state, store, screen)
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
