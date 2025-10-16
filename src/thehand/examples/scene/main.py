import pygame

from thehand.core import SceneManager, State
from thehand.examples.scene.basic_scene import BasicScene

DEFAULT_WINDOW_SIZE: tuple[int, int] = (1280, 720)


def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Example Game")

    screen = pygame.display.set_mode(DEFAULT_WINDOW_SIZE)

    state = State()
    state.debug_mode = True

    scene_manager = SceneManager(state)

    scene1 = BasicScene("scene1", screen, state)
    scene2 = BasicScene("scene2", screen, state)
    scene3 = BasicScene("scene3", screen, state)

    scene_manager.add(scene1)
    scene_manager.add(scene2)
    scene_manager.add(scene3)
    scene_manager.run("scene1")

    scene1 >> scene2 >> scene3

    scene_manager()


if __name__ == "__main__":
    main()
