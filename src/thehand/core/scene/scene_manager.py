import pygame

from thehand.core.scene.scene import Scene
from thehand.core.state import StateManager


class SceneManager:
    """
    Manage scenes.
    Run only one scene at a time.
    Do scene operations: add, remove, reload, next, previous and handle transition.
    """

    def __init__(self, state: StateManager | None = None) -> None:
        self.state: StateManager = state if isinstance(state, StateManager) else StateManager()

        self.scenes: dict[str, Scene] = {}
        self.current_scene: Scene | None = None

        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

    def run(self):
        if not self.current_scene:
            raise AttributeError("No scene selected")

        self.current_scene.handle_events()
        self.current_scene.update()
        self.current_scene.render()

        self.clock.tick(self.state.FPS)

    def set_current_scene(self, name: str) -> None:
        if not self.scenes.get(name):
            raise NameError(f'Scene "{name}" not found!')
        self.current_scene = self.scenes[name]

    def add(self, scene: Scene) -> None:
        self.scenes[scene.name] = scene

    def remove(self, name: str) -> None:
        del self.scenes[name]

    def reload(self) -> None:
        pass

    def next(self) -> None:
        pass

    def prev(self) -> None:
        pass
