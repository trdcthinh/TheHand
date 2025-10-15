import pygame

from thehand.core.scene.scene import Scene
from thehand.core.state import State


class SceneManager:
    def __init__(self, state: State | None = None) -> None:
        self.state: State = state if isinstance(state, State) else State()

        self.scenes: dict[str, Scene] = {}
        self.current_scene: Scene | None = None

        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

    def __call__(self):
        if len(self.scenes) == 0:
            raise IndexError("No scene!")

        if not self.current_scene:
            raise AttributeError("No current scene")

        while self.current_scene:
            self.current_scene.handle_events()
            self.current_scene.update()
            self.current_scene.render()

            self.clock.tick(self.state.FPS)

            if self.current_scene.done:
                self.next()

    def run(self, scene: str) -> None:
        if not self.scenes.get(scene):
            raise NameError(f'Scene "{scene}" not found!')
        self.current_scene: Scene = self.scenes[scene]

    def add(self, scene: Scene) -> None:
        self.scenes[scene.name] = scene

    def next(self) -> None:
        self.current_scene = self.current_scene.next_scene
