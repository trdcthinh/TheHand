import pygame

from thehand.engine.scene.scene import Scene


class SceneManager:
    """
    Manage scenes.
    Run only one scene at a time.
    Do scene operations: add, remove, reload, next, previous and handle transition.
    """

    def __init__(self):
        self.scenes: dict[str, Scene] = {}
        self.current_scene: Scene = None

        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

    def run(self):
        self.current_scene.handle_events()
        self.current_scene.update()
        self.current_scene.render()
        self.clock.tick(60)
        pass

    def set_current_scene(self, name: str):
        if not self.scenes.get(name):
            raise NameError(f'Scene "{name}" not found!')
        self.current_scene = self.scenes[name]

    def add(self, scene: Scene):
        self.scenes[scene.name] = scene

    def remove(self):
        pass

    def reload(self):
        pass

    def next(self):
        pass

    def prev(self):
        pass
